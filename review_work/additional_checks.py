exec(open('review_work/validate.py',encoding='utf-8').read().split("Path('review_work/validation.json')")[0])
g=s.groupby(['date','region','sku']).quantity.sum().unstack(['region','sku']).reindex(dates).fillna(0)
top=g.loc[:'2025-06-30'].sum().nlargest(10).index
result=[]
for method in ['naive','seasonal_naive_7','MA7','MA28']:
 actual=[]; pred=[]
 for origin in pd.date_range('2025-06-30','2025-09-22',freq='7D'):
  hist=g.loc[:origin,top]
  y=g.loc[pd.date_range(origin+pd.Timedelta(days=1),periods=7),top].to_numpy()
  if method=='seasonal_naive_7': p=hist.iloc[-7:].to_numpy()
  else:
   n={'naive':1,'MA7':7,'MA28':28}[method]
   p=np.tile(hist.tail(n).mean().to_numpy(),(7,1))
  actual.append(y); pred.append(p)
 a=np.array(actual); p=np.array(pred); err=p-a
 result.append({'model':method,'origins':len(actual),'MAE':np.abs(err).mean(),'WAPE_pct':100*np.abs(err).sum()/a.sum(),'MAPE_positive_pct':100*np.mean(np.abs(err)[a>0]/a[a>0]),'positive_coverage':np.mean(a>0),'bias':err.mean(),'WAPE_weekly_total_pct':100*np.abs(err.sum(axis=1)).sum()/a.sum()})
print('BASELINES_VALIDATION',json.dumps(result,ensure_ascii=False,indent=2))
Path('review_work/baseline_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('TOP10_TRAIN',list(top))
print('SUCCESS_SKU_ORDERS',s.sku.value_counts().to_dict())
print('UTC_TO_VN_DATE_CHANGES',int((d.od.dt.tz_convert('Asia/Ho_Chi_Minh').dt.date!=d.od.dt.date).sum()))
print('SKU_DAYS_ZERO_CELLS',int(g.eq(0).sum().sum()))
print('LAST7_DETAIL_ZERO',int((s[s.date.ge('2025-12-25')].groupby(['carrier','sku','product_type']).quantity.sum().reindex(pd.MultiIndex.from_product([sorted(d.carrier.unique()),sorted(d.sku.unique()),sorted(d.product_type.unique())]),fill_value=0)==0).sum()))
daily=s.groupby(['date','sku']).quantity.sum().unstack('sku').reindex(dates).fillna(0).join(c.set_index('date'))
for label,sku in [('Quốc khánh 2/9','D3G-5D'),('Tết Nguyên Đán','D5G-7D'),('Tết Nguyên Đán','D20G-30D')]:
 mask=daily.holiday_name.eq(label)
 print('HOLIDAY_RATIO',label,sku,daily.loc[mask,sku].mean()/daily.loc[daily.is_holiday.eq(0),sku].mean())
for sku in ['D1G-3D','UL-5D']:
 print('SUMMER_RATIO',sku,daily.loc[daily.is_summer_season.eq(1),sku].mean()/daily.loc[daily.is_summer_season.eq(0),sku].mean())
