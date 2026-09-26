# Data contract v0.3 — Quantity sold

Cập nhật **26/09/2026** theo [DECISIONS S2/S4–S6](DECISIONS.md). Target đã xác nhận: **số lượng bán thành công theo ngày đặt UTC**. Activation là dữ liệu tham khảo.

## 1. Target, grain và phạm vi

```text
order_date = DATE(order_datetime sau khi parse UTC)
route = (destination_country, carrier)
quantity_sold[order_date, route, sku]
    = SUM(quantity WHERE order_status = 'success')
quantity_sold_route[order_date, route]
    = SUM(quantity_sold qua tất cả SKU)
```

- **Đơn vị:** SIM/gói bán ra; không phải số đơn hay số kích hoạt. Không lọc success theo activation.
- **Phạm vi:** tất cả 10 SKU trên mọi tuyến hợp lệ. Output cơ sở gộp hai product_type; khi tách type phải giữ tổng. Tồn kho luôn phân biệt eSIM/physical_SIM.
- **Top 10 tuyến:** xếp giảm dần tổng quantity success trong train, cộng mọi SKU/type; khóa danh sách và cutoff trước validation/test. Tie-break kỹ thuật đề xuất: country rồi carrier tăng dần. Top 10 chỉ dùng chấm KPI MAPE ≤20%, không thu hẹp forecast.
- **Lưới ngày:** 01/01/2024–31/12/2025, 731 ngày gồm 29/02/2024. Khóa `DAILY_DEMAND`: target_version + order_date + series_key; series_key giải ra country/carrier/SKU.
- Country 1–n Carrier; Region 1–n Country. Trong file có 46 tuyến và 460 cặp tuyến × SKU; không nhân chéo 18 country với 46 carrier. Đây là thống kê toàn kỳ, không chứng minh offering đã mở bán ở mọi origin.
- **[CỨNG]** Zero chỉ được điền khi giả định dữ liệu đã nạp đủ và offering đang được bán. Khai báo catalog/availability dùng tại origin; nếu giả định catalog cố định cho replay, ghi thành scenario. Không lấy lần xuất hiện tương lai làm bằng chứng đang bán trong quá khứ.

**Quantity bán quan sát được không đồng nghĩa nhu cầu tiềm ẩn hoặc lượng trừ kho thật.** CSV thiếu availability/stockout. M3 có thể giả định một đơn vị bán trừ một đơn vị kho theo order_date; giả định này phải có version.

## 2. Dữ liệu đã kiểm chứng

| Nội dung | Giá trị |
|---|---:|
| Orders | **100.000 đơn hàng**, 20 cột; 0 order_id trùng |
| Thời gian order UTC | **01/01/2024–31/12/2025 (731 ngày)** |
| Quốc gia đích / carrier / region / SKU | **18 / 46 / 8 / 10** |
| eSIM / physical_SIM | 73.092 / 26.908 dòng, mọi trạng thái |
| Đơn success | **93.104 đơn** |
| SUM(quantity) success | **118.296 đơn vị** |

**10 SKU:** D1G-3D, D3G-5D, D5G-7D, D10G-10D, D15G-15D, D20G-30D, UL-5D, UL-7D, UL-15D, UL-30D.

| order_status | Số đơn | Tổng quantity | Activation rỗng |
|---|---:|---:|---:|
| success | 93.104 | 118.296 | 0 |
| failed | 2.330 | 2.958 | 2.330 |
| timeout | 2.214 | 2.814 | 2.214 |
| refunded | 1.205 | 1.520 | 0 |
| pending | 1.147 | 1.484 | 1.147 |

Đối soát tổng quantity success phải giữ **118.296** khi đổi cách nhóm trên toàn cửa sổ order. Số dòng grid/độ thưa phải tính đúng grain: 58.480 dòng và 53,0301% zero của review thuộc **Region × SKU v0.1**, không phải tuyến × SKU. Benchmark Top 10 cũ cũng không phải Top 10 tuyến.

## 3. Schema orders

Raw bất biến; tên cột dưới đây là tên gốc. `order_date` và ID mapping là cột dẫn xuất.

| Cột | Kiểu / ý nghĩa / kiểm tra |
|---|---|
| order_id | Text, không rỗng/trùng |
| order_datetime | Datetime UTC có hậu tố Z; tạo order_date dùng cho target |
| activation_datetime | Datetime UTC nullable; giữ NULL, không impute; không trước order; chỉ tham khảo |
| product_type | eSIM hoặc physical_SIM |
| destination_country | Nước đích sử dụng SIM, không phải nơi bán |
| region | Khu vực gộp các nước đích, không suy thành vị trí kho |
| carrier | Nhà mạng tại nước đích; chiều đối tác cho inventory/config |
| sku | Một trong 10 mẫu gói; chưa đủ nhận diện offering thay thế |
| plan_type | fixed hoặc unlimited, cố định theo SKU |
| data_gb | Thuộc tính SKU; không tự hiểu unlimited có hard cap này |
| validity_days | Số ngày dùng gói, không phải hạn lưu kho/kích hoạt |
| quantity | Số nguyên; quan sát 1–4, không áp khoảng này thành giới hạn nghiệp vụ vĩnh viễn |
| unit_price_vnd, unit_cost_vnd | Số VND dương |
| gross_revenue_vnd | quantity × unit_price_vnd; không dùng revenue cùng ngày làm feature |
| sales_channel, payment_method | Kênh bán và phương thức thanh toán |
| customer_id | Mã khách; không dùng tổng hợp toàn kỳ làm feature |
| customer_type | Giữ raw để audit; **không dùng phân tích, feature hoặc logic** |
| order_status | success, failed, timeout, refunded, pending; chỉ có trạng thái cuối |

**[CỨNG]** Kiểm tra bộ ba carrier/country/region khi nạp; FK riêng không ngăn mapping mâu thuẫn. Các phụ thuộc quan sát không phải cam kết bất biến tương lai. Không dùng `is_suspected_anomaly`, `anomaly_note` của calendar trong logic/feature.

## 4. Nguồn và metadata

| Loại | Ví dụ | Cần lưu |
|---|---|---|
| Quan sát | Orders được cấp | Raw/checksum, thời gian và trạng thái cuối |
| Dẫn xuất | Target, mapping, lag/rolling/share | Công thức, cutoff, version; chỉ lịch sử đã biết tại origin |
| Lịch tự dựng | Thứ/tháng, lễ Việt Nam/mùa du lịch | Nguồn, quy tắc nhãn, version; tác động lễ cần ablation |
| Giả định scenario | Stock, L/R/MOQ/SS/ROP, ETA, reservation, chi phí, EOL | Source, lý do, status “cần mentor xác nhận” nếu chưa duyệt, scenario_id/version, seed nếu có |
| Kết quả mô phỏng | Stock biến động, lượng nhập, stockout, fill rate | Scenario, policy/run và cách tính; nhãn mô phỏng |

**[CỨNG]** Stock/config thiếu có trạng thái riêng, không âm thầm điền 0. Chỉ có orders được cấp; không chờ nguồn kho/config/receipt thật. Carrier là scope cấu hình đối tác; orders không xác định điều khoản hợp đồng, stock hay procurement lead time thực.

Metadata tối thiểu: `target_version=v0.3`, `event_date_basis=order_date`, `timezone=UTC`, `status_filter=success`, `unit=quantity`, `grain=route_sku`, observation_start/end, data_cutoff và source checksum. Forecast thêm run_id, origin, horizon, model_version, catalog_version và config version nếu áp dụng.

## 5. Quy tắc thời gian và tham khảo activation

- **[CỨNG]** Khóa UTC ở mọi module/ghép lịch; đổi timezone/filter/grain phải version hóa và tái lập. Bán tại Việt Nam không tự đổi quy ước ngày sang giờ Việt Nam.
- CSV chỉ có trạng thái cuối: backtest giả định nhãn đủ chín tại cutoff; không chứng minh success/refunded đã được biết lúc đặt. Không dùng trạng thái hoặc activation tương lai làm feature.
- Feature chỉ nhìn dữ liệu tới origin; direct training row chỉ hợp lệ khi toàn bộ nhãn đã nằm trước cutoff huấn luyện. Calendar phải phủ ngày forecast và có nguồn/version.
- Replay lịch sử theo ngày order; forecast sau 31/12/2025 chưa có actual **bán hàng** trong file. Không dùng ngày làm dự án làm ngày dữ liệu.
- **v0.2 activation đã hạ thành tham khảo tùy chọn**. Raw activation ngoài khoảng order vẫn giữ; muộn nhất 14/01/2026. Nếu phân tích riêng, khai báo filter/cửa sổ và lệch mẫu đầu/cuối; không coi ngày activation cuối là chứng cứ đủ quan sát.
- Activation thiếu 5.691 dòng, nhưng success không thiếu; lý do chọn order là xác nhận nghiệp vụ của mentor. Activation lag không phải procurement lead time.
- Refunded bị loại khỏi target chính. Sensitivity success+refunded, nếu chạy, mang nhãn riêng và không chứng minh có hoàn kho.
- Với EOL, failed+timeout = 4,544%; failed+timeout+pending = 5,691%; mọi non-success = 6,896%. Pending chưa chắc lỗi. Khai báo tử/mẫu/cửa sổ/số đơn tối thiểu trước khi áp ngưỡng.
- Hệ số mùa vụ cũ chưa tái lập được: cần công thức/cửa sổ/mẫu số/trọng số/xử lý xu hướng và code trước khi sử dụng.

Nguồn số liệu: [Review A1–A4](../Review_SIGMA_M2_M3.md). Luật chi tiết ở [AGENTS](../AGENTS.md), cách đo ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md).
