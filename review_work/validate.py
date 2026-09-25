import pandas as pd
import numpy as np
import json
from pathlib import Path

d=pd.read_csv('data/sigma_sim_data_orders.csv')
c=pd.read_csv('data/sigma_calendar_dim_2024_2025.csv',usecols=lambda x:x not in ['is_suspected_anomaly','anomaly_note'])
d['od']=pd.to_datetime(d.order_datetime,utc=True)
d['ad']=pd.to_datetime(d.activation_datetime,utc=True)
d['date']=d.od.dt.floor('D').dt.tz_localize(None)
s=d[d.order_status.eq('success')].copy()
dates=pd.date_range('2024-01-01','2025-12-31')
out={}
def add(k,v): out[k]=v
add('shape',d.iloc[:,:20].shape)
add('unique',d.iloc[:,:20].nunique().to_dict())
add('nulls',d.iloc[:,:20].isna().sum().to_dict())
add('duplicates',{'rows':int(d.iloc[:,:20].duplicated().sum()),'order_id':int(d.order_id.duplicated().sum())})
add('range',{'order':[str(d.od.min()),str(d.od.max())],'activation':[str(d.ad.min()),str(d.ad.max())],'days':d.date.nunique()})
for col in ['order_status','product_type','plan_type','quantity']:
 add(col,d[col].value_counts().to_dict())
add('activation_by_status',pd.crosstab(d.order_status,d.ad.isna()).to_dict())
add('revenue_mismatch',int((d.gross_revenue_vnd!=d.quantity*d.unit_price_vnd).sum()))
add('nonpositive_price_cost',int(((d.unit_price_vnd<=0)|(d.unit_cost_vnd<=0)).sum()))
add('mapping', {a+'->'+b:d.groupby(a)[b].nunique().value_counts().to_dict() for a,b in [('carrier','destination_country'),('destination_country','region'),('destination_country','carrier'),('region','destination_country'),('sku','plan_type'),('sku','data_gb'),('sku','validity_days')]})
add('catalog',d.groupby('sku').agg(plan=('plan_type','first'),gb=('data_gb','first'),days=('validity_days','first'),orders=('order_id','size'),price=('unit_price_vnd','mean')).to_dict('index'))
add('success_qty',int(s.quantity.sum()))
add('status_qty',d.groupby('order_status').quantity.sum().to_dict())
def maxzero(x):
 a=x.eq(0); return int(a.groupby((~a).cumsum()).sum().max())
for keys in [['sku'],['region','sku'],['carrier','sku'],['region','carrier','sku','product_type']]:
 g=s.groupby(['date']+keys).quantity.sum().unstack(keys).reindex(dates).fillna(0)
 z=g.eq(0).mean(); runs=g.apply(maxzero); sums=g.sum(); top=sums.nlargest(10).index
 add('_'.join(keys),{'shape':g.shape,'zero_mean':z.mean(),'zero_min':z.min(),'zero_max':z.max(),'maxzero_mean':runs.mean(),'maxzero_max':runs.max(),'no_zero_series':int((z==0).sum()),'top10_maxrun':runs.loc[top].max(),'top50_maxrun':runs.loc[sums.nlargest(50).index].max(),'top10_share':sums.loc[top].sum()/sums.sum()})
 if keys==['region','sku']:
  tab=pd.DataFrame({'quantity':sums,'zero_ratio':z,'max_zero_run':runs}).sort_values('quantity',ascending=False)
  tab.to_csv('review_work/series_validation.csv')
  add('region_sku_extremes',{'top10':tab.head(10).reset_index().to_dict('records'),'sparsest':tab.sort_values('zero_ratio',ascending=False).head(5).reset_index().to_dict('records')})
  add('last_month_sku',s[s.date.ge('2025-12-01')].groupby('sku').quantity.sum().to_dict())
  add('product_types_per_region_sku',s.groupby(['region','sku']).product_type.nunique().value_counts().to_dict())
lag=(d.ad-d.od).dt.total_seconds()/86400
add('activation_lag',{'all':lag.describe(percentiles=[.5,.9,.95,.99]).to_dict(),'success':lag[s.index].describe(percentiles=[.9]).to_dict(),'negative':int((lag<0).sum()),'same_day_success':int((s.ad.dt.floor('D')==s.od.dt.floor('D')).sum())})
add('annual',s.groupby(s.date.dt.year).agg(orders=('order_id','size'),quantity=('quantity','sum')).to_dict('index'))
add('region_qty',s.groupby('region').quantity.sum().to_dict())
add('sku_finance',s.groupby('sku').agg(quantity=('quantity','sum'),revenue=('gross_revenue_vnd','sum')).assign(qty_share=lambda x:x.quantity/x.quantity.sum(),rev_share=lambda x:x.revenue/x.revenue.sum()).to_dict('index'))
c['date']=pd.to_datetime(c.date)
add('calendar',{'rows':len(c),'duplicate_dates':int(c.date.duplicated().sum()),'missing_dates':len(dates.difference(c.date)),'dow_errors':int((c.day_of_week!=c.date.dt.dayofweek+1).sum()),'dow_name_errors':int((c.day_of_week_name!=c.date.dt.day_name().str[:3]).sum()),'month_errors':int((c.month!=c.date.dt.month).sum()),'summer_errors':int((c.is_summer_season!=c.date.dt.month.isin([6,7,8])).sum()),'holidays':c.groupby('holiday_name').size().to_dict(),'flag_counts':c[['is_holiday','is_pre_holiday','is_post_holiday','is_summer_season']].sum().to_dict(),'holiday_label_mismatch':int((c.is_holiday.eq(1)!=c.holiday_name.notna()).sum())})
# Little's-law approximation versus actual end-of-day outstanding units.
open_units=[]
for dt in pd.date_range('2024-02-01','2025-12-01',tz='UTC'):
 t=dt+pd.Timedelta(days=1)
 open_units.append(int(s.loc[(s.od<t)&(s.ad>=t),'quantity'].sum()))
add('sold_not_activated_daily',{'mean':np.mean(open_units),'min':min(open_units),'max':max(open_units)})
Path('review_work/validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=lambda x:x.item() if hasattr(x,'item') else str(x)),encoding='utf-8')
print(Path('review_work/validation.json').read_text(encoding='utf-8'))
