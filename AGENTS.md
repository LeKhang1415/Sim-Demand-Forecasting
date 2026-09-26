# Hướng dẫn AI coding agent — SIGMA

Áp dụng khi viết/sửa pipeline, feature, model, backtest, allocation, inventory, EOL và output. Checklist giữ các lỗi/ràng buộc **[CỨNG]** của review, cập nhật nghiệp vụ theo xác nhận mentor do người dùng cung cấp ngày 26/09/2026; không biến **[MỀM] / [XÁC NHẬN]** thành luật nghiệp vụ đã duyệt.

## Thứ tự nguồn và trạng thái quyết định

- [ ] Đọc [PROJECT_OVERVIEW](docs/PROJECT_OVERVIEW.md), [DECISIONS.md](docs/DECISIONS.md) và [Review_SIGMA_M2_M3.md](Review_SIGMA_M2_M3.md). Xác nhận mới của mentor qua người dùng ưu tiên hơn ảnh đề bài và đề xuất cũ mâu thuẫn; review vẫn là nguồn cho số liệu đã kiểm chứng và lỗi kỹ thuật. Không dùng phần D1/D2/D3 lịch sử để ghi đè quyết định cập nhật.
- [ ] Giữ ý nghĩa nhãn **[CỨNG] / [MỀM] / [XÁC NHẬN]**. S1–S6 trong DECISIONS là các xác nhận hiện hành; target/filter/đơn vị/phạm vi dự báo và nguyên tắc cấu hình riêng carrier đã chốt. Các giá trị/default còn mở vẫn là **đề xuất — cần mentor xác nhận**. Không coi quyền dựng giả định là mentor đã duyệt mọi giá trị.
- [ ] **Phạm vi đã xác nhận:** chỉ có orders được cấp. Tự dựng dữ liệu dẫn xuất và config/scenario; không xin/chờ inventory, supplier config, receipts, EOL hoặc order mới như điều kiện triển khai dự án.
- [ ] Tách quan sát, dẫn xuất, giả định và kết quả mô phỏng theo [DATA_CONTRACT v0.3](docs/DATA_CONTRACT.md). Dẫn xuất có công thức/cutoff; giả định có lý do/source/status/version/scenario và seed nếu có. Không suy stock/L/MOQ/chi phí thật chỉ từ orders.
- [ ] **Target đã xác nhận:** SUM(quantity) WHERE order_status='success' theo order_date UTC; activation chỉ tham khảo, không là target hay điều kiện lọc success. Output cho tất cả 10 SKU × tuyến (destination_country, carrier) hợp lệ; tổng tuyến bằng cộng SKU/type. Top 10 chọn theo tổng quantity success trong train, chỉ dùng chấm KPI, không thu hẹp phạm vi forecast.
- [ ] **Nghiệp vụ đã xác nhận:** chỉ bán cho khách ở Việt Nam đi du lịch quốc tế. Country là nước sử dụng, carrier là nhà mạng tại nước đích, region gộp các nước đích; không suy thành nơi bán hoặc vị trí kho.
- [ ] **Đối soát dữ liệu:** 100.000 đơn, 18 nước đích, 46 carrier, 8 region, 10 SKU, 2 product_type; 01/01/2024–31/12/2025 có 731 ngày; 93.104 đơn success, 118.296 đơn vị. Không đồng nhất số đơn với quantity.
- [ ] Giữ mục tiêu MAPE ≤20% ở Top 10 tuyến và cảnh báo trước ≥7 ngày. Báo đạt/chưa đạt theo cách đo thống nhất, không bỏ KPI hoặc tự coi metric bổ sung là thay thế đã được chấp thuận.
- [ ] Mọi default SS/ROP, L/R/MOQ, service target, cửa sổ phân bổ, hệ số mùa vụ/chuyển đổi EOL/cold-start và scenario cần nguồn + trạng thái “cần mentor xác nhận” trong code/config khi chưa được duyệt. Không hard-code như luật doanh nghiệp hoặc tự ghi người/ngày phê duyệt.
- [ ] **[CỨNG]** Không dùng `customer_type` làm feature/phân tích; không dùng `is_suspected_anomaly`, `anomaly_note` trong logic/feature. Raw có thể giữ bất biến cho audit; tên cột trong schema không phải sự cho phép sử dụng.
- [ ] Không suy từ dữ liệu demo sang hiệu quả vận hành thật. Inventory/config giả định phải có source, scenario_id, version và nhãn minh họa; thiếu input có trạng thái riêng. (B8, D3, E)

## Dữ liệu, target và thời gian

- [ ] **[CỨNG] A2.1:** Lưới order-date UTC gồm 731 ngày và ngày nhuận 29/02/2024, không dùng “730 ngày” của PDF. Số dòng/độ thưa phải tính đúng grain; 58.480 dòng của Region × SKU v0.1 không phải lưới tuyến × SKU v0.3.
- [ ] **[CỨNG] A2.2:** Country 1–n Carrier; Region 1–n Country. Carrier → country → region là phụ thuộc một chiều trong dataset, không phải song ánh hoặc bất biến nghiệp vụ tương lai.
- [ ] **[CỨNG] A2.3:** Phân biệt số dòng mọi trạng thái, số đơn success và SUM(quantity) success. Không gắn nhãn “số đơn thành công” cho số liệu SKU toàn bộ trạng thái.
- [ ] **[CỨNG] A2.6/B7.f:** Hệ số mùa vụ chưa tái lập được theo định nghĩa công bố; không dùng như tham số chắc chắn. Cần công thức/cửa sổ/mẫu số/trọng số/xử lý xu hướng và code trước khi dùng; tỷ số kiểm tra độ nhạy không thay hệ số chính thức.
- [ ] Giữ raw bất biến; activation NULL vẫn NULL, không impute thành ngày đặt. Kiểm tra bộ ba carrier/country/region nếu cùng lưu, vì FK riêng không ngăn dữ liệu mâu thuẫn. Khoảng quantity quan sát không phải CHECK nghiệp vụ vĩnh viễn. (A1, B4, B8)
- [ ] **[CỨNG] B1:** Lý do chọn order/quantity sold là xác nhận nghiệp vụ của mentor, không phải vì thiếu activation toàn bộ orders; success có activation đầy đủ. Khai báo riêng giả định liên hệ lượng bán với trừ kho mô phỏng.
- [ ] **[CỨNG] B1:** Không đồng nhất lượng bán quan sát với nhu cầu tiềm ẩn hoặc stock consumption. CSV thiếu availability/stockout; không dựng nhãn “không có nhu cầu” như sự thật.
- [ ] **[CỨNG] B1:** Activation lag không phải procurement lead time. Không dùng lag này để điền L khi thiếu nguồn vận hành.
- [ ] Refunded bị loại khỏi target chính đã chốt. Success+refunded chỉ là sensitivity tùy chọn có nhãn riêng; activation không chứng minh kho đã được hoàn. Không đồng nhất lượng bán/kích hoạt với dòng hàng trả lại. (A1, B1, contract v0.3)
- [ ] **[CỨNG] B1/A3.6:** Khóa UTC cho order_date và activation_date, không đổi giữa module/ghép lịch. Đổi timezone/filter/grain phải version hóa và tái lập, không đổi âm thầm.
- [ ] **[CỨNG] B1:** Lưu data_cutoff, timezone và target version; công bố giới hạn point-in-time. Trạng thái cuối không chứng minh pending/refunded đã biết lúc đặt; backtest đang giả định nhãn đủ chín.
- [ ] Nếu phân tích activation tham khảo, giữ sự kiện ngoài khoảng order và kiểm tra lệch mẫu đầu/cuối. Ngày activation cuối không chứng minh dữ liệu đầy đủ tới đó; không dùng cửa sổ này thay cửa sổ target bán hàng. (A3.5, contract v0.3)
- [ ] **[CỨNG] B2, cập nhật phạm vi:** Phân biệt grain model, output tuyến theo đề bài và stock item. Region × SKU là phương án gộp v0.1. Nếu dùng cấp gộp/cấp con, vẫn phải xuất đủ tuyến × SKU và cộng về tổng tuyến để chấm KPI quantity sold.
- [ ] **[CỨNG] B2:** Chỉ điền zero khi giả định dữ liệu đã nạp đủ và mặt hàng đang được bán. Khi có thông tin, phân biệt zero thật/chưa mở bán/tạm dừng/thiếu dữ liệu/hết hàng; không nội suy zero thật thành nhu cầu dương.
- [ ] Không dùng ngày làm dự án làm ngày dữ liệu. Phạm vi là replay lịch sử/mô phỏng; không chờ order mới hoặc gọi dữ liệu cũ là forecast vận hành hiện tại. Sau 31/12/2025 chưa có actual bán hàng trong file; activation muộn hơn không bổ sung actual cho target này. (D2 cập nhật)

## Feature, horizon và chống leakage

- [ ] **[CỨNG] B1–B3:** Không đưa feature hoặc nhãn chứa thông tin sau origin vào đầu vào dự báo. Nhãn huấn luyện origin+h chỉ được sử dụng khi đã nằm trước cutoff của tập huấn luyện.
- [ ] **[CỨNG] B2:** Lag/rolling nằm trong từng chuỗi và chỉ lấy lịch sử đã biết. Thiết kế ngày t từ dữ liệu tới t−1 phải shift trước khi rolling/tổng hợp; không lẫn chuỗi hoặc tính bằng target của ngày cần dự báo.
- [ ] **[CỨNG] B2:** Chấm horizon thật nhiều bước; không dự báo bước sau với lag_1 chứa actual tương lai. Direct dùng thống kê tại origin + horizon_day/lịch ngày dự báo. Nếu đổi sang recursive, thay actual chưa biết bằng forecast trong training/evaluation tương ứng; direct vẫn là **[MỀM]**, không phải lựa chọn duy nhất.
- [ ] **[CỨNG] B1–B2:** Không dùng activation/trạng thái tương lai, giá bình quân của đơn trong ngày cần dự báo, revenue hoặc quantity cùng ngày làm feature. Giá/khuyến mãi tương lai chỉ dùng nếu đã biết tại origin.
- [ ] Không đưa một carrier categorical vào dòng Region × SKU có nhiều carrier. Tỷ trọng lịch sử nếu dùng phải tính tới origin; M2 chưa cần bước này. Không dùng CUSTOMER tổng hợp toàn kỳ làm feature. (B2, B4)
- [ ] Calendar phải phủ ngày forecast và có nguồn/phiên bản; không gọi calendar tự dựng là đã duyệt. Khách mua ở Việt Nam; feature lễ Việt Nam/mùa du lịch là **[MỀM]**, cần nguồn và ablation; không tự chọn lịch nước chi phối chỉ từ điểm đến. (A2.4, B2, B4)
- [ ] **[CỨNG] B3:** Không chọn Top 10, feature, cửa sổ phân bổ hoặc ngưỡng EOL bằng test/future; thống kê toàn kỳ trong review chỉ là EDA.
- [ ] Chỉ đưa direct training row vào khi toàn bộ nhãn của row đã nằm trước cutoff; chỉ chấm horizon đầy đủ trong partition. Cố định lịch refit trước test; actual test đã trôi qua có thể dùng ở origin mới, actual sau origin không được dùng. Không tuning lại bằng final test. (D2)

## Metric và diễn giải kết quả

- [ ] **[CỨNG] B3:** MAPE không tính khi actual=0; không chèn epsilon tùy ý. Dùng tên MAPE_positive, luôn báo số điểm/tổng điểm và coverage, cùng MAE/WAPE; không bỏ zero rồi gọi là MAPE toàn bộ.
- [ ] WAPE/bias có mẫu số bằng 0 thì N/A, báo MAE/forecast excess riêng. MASE/RMSSE chuẩn hóa bằng train; mẫu số train bằng 0 thì N/A. (B3)
- [ ] Không trình metric tuần/tổng horizon như metric ngày; không chọn model chỉ vì MAE của nhóm rất thưa. Xét bias, sai số cộng dồn và hệ quả stockout; chấm các region/nhóm thưa, không chỉ Top 10. (A3–A4, B2–B3)
- [ ] Benchmark A4 là order-date × Region × SKU v0.1, không chứng minh đạt/không thể đạt KPI quantity sold theo tuyến v0.3. Chạy lại benchmark đúng grain; chấm và chọn model/fallback theo tuyến. Không sửa metric để “đạt”; hoàn thành kỹ thuật không tự đồng nghĩa nghiệm thu KPI. (A4, D1.8, D2 cập nhật)

## Khóa bảng, metadata và phân bổ

- [ ] **[CỨNG] B4:** REGION_INVENTORY có snapshot + region + carrier + SKU + product_type, hoặc stock_item_id biểu diễn đủ. Lưu snapshot timestamp/source/scenario; định nghĩa stock khả dụng, đã giữ chỗ và hàng không thể bán. Không dùng chung một tồn kho cho nhiều nhà cung cấp/type khi tính theo Mục 8.5.
- [ ] **[CỨNG] B4:** Thống nhất PK FORECAST_RESULT, run_date không đủ phân biệt rerun. Theo schema v0.3 đề xuất, dùng run_id + series_key + forecast_date; mỗi run gắn một target/grain version, series_key giải ra route/cấp con. Truy vết model_version/cutoff/filter; không trộn activation với order-date.
- [ ] **[CỨNG] B4:** REORDER_RECOMMENDATION đủ carrier/product_type; liên kết run forecast, snapshot, config/allocation/rule version và scenario. Không FK một khuyến nghị cộng nhiều ngày vào một dòng forecast ngày đơn lẻ.
- [ ] **Đã xác nhận:** SS/ROP/MOQ/ngưỡng cảnh báo và rule nhập cấu hình riêng từng carrier/đối tác; không dùng một bộ tham số chung. SUPPLIER_CONFIG có scope carrier/type/SKU, hiệu lực/version, default/override rõ; thiếu config không mượn carrier khác. Giá trị cụ thể, cơ sở so ngưỡng và toán tử < hoặc ≤ cần source/status. `sku='*'` không phải SKU thật để ép qua FK; kiểm tra uniqueness/hiệu lực. (B4)
- [ ] **[CỨNG] B4:** Lifecycle theo đúng offering/stock item; không EOL SKU chung toàn hệ thống vì một carrier dừng. Thống nhất vai trò replace_sku/successor_sku; cascade đúng phạm vi thực sự.
- [ ] **[CỨNG] B5.1:** Share chỉ dùng lịch sử tới origin; tử/mẫu cùng parent/target/cửa sổ. Parent route hoặc route × SKU theo cấp phân bổ quantity sold; region/SKU chỉ cho nhánh gộp có backtest. Không chuyển share giữa target mà thiếu nhãn giả định/kiểm thử.
- [ ] **[CỨNG] B5.2:** Lọc offering hợp lệ; phân biệt chưa có lịch sử và không còn cung cấp. Mẫu số các cửa sổ fallback bằng 0 thì allocation_unavailable hoặc mapping demo đã cấu hình, không chia cho 0.
- [ ] **[CỨNG] B5.3:** Chỉ ép tổng share=1 khi toàn bộ nhu cầu cha còn phục vụ được. Khi EOL mất khách, tách phần giữ được và phần không phục vụ; không ép toàn bộ sang carrier còn lại.
- [ ] **[CỨNG] B5.4:** Không tự thay country cùng region hoặc đổi eSIM sang physical_SIM; kiểm tra điểm đến, thiết bị, gói/quyền sử dụng và nguồn cung.
- [ ] **[CỨNG] B5.5:** Forecast giữ số thực; chỉ làm tròn lượng nhập. Phân bổ số nguyên nếu cần phải có quy tắc phần dư thống nhất để giữ tổng.
- [ ] **[CỨNG] B5.6:** Bất định cấp con gồm sai số share; không gọi quantile cha nhân share là quantile đúng của con. Backtest cả cấp nhận phân bổ. (B5)

## Tồn kho, Safety Stock, ROP và cảnh báo

- [ ] **[CỨNG] B6.1:** Không triển khai lẫn hai công thức nhập của PDF khi chưa định nghĩa kỳ bảo vệ. Chốt policy, L, R, IP, trigger và target; không trộn periodic review với continuous (s,S). Không tự gọi ROP+forecast_7d là đếm đôi khi chưa xét policy.
- [ ] L/R là ngày cùng đơn vị forecast; IP dùng usable on-hand, receipts được công nhận và nghĩa vụ chưa đáp ứng. Không trừ reservation hai lần hoặc trùng backorder/reservation. Công thức đề xuất nằm ở [ARCHITECTURE](docs/ARCHITECTURE.md), vẫn cần mentor xác nhận. (B6.2)
- [ ] SS theo số ngày là heuristic demo, không phải service level đã hiệu chỉnh. Residual/quantile phải từ backtest không leakage, đúng horizon/cấp; không cộng quantile ngày để thành quantile tổng. Công thức chuẩn có giả định về nhu cầu/L; không áp như luật cho chuỗi cực thưa/L biến động. Cycle service level không đồng nhất fill rate. (B6.3)
- [ ] **[CỨNG] B6.4:** velocity_7d=0 không tự suy ra OK/an toàn hoặc mặc định SS/ROP là bằng chứng an toàn. Dùng forecast cộng dồn/fallback; thiếu bằng chứng thì “chưa đủ dữ liệu”. days_of_cover=N/A khi velocity=0, không gán 0 hoặc tạo ngày cạn giả.
- [ ] **[CỨNG] B6.5:** Thiếu stock/config không phải stock/config=0. q_raw=0 thì q=0, không nâng MOQ. MOQ không đồng nghĩa bội số đóng gói; kiểm tra hạn dùng/sức chứa/EOL và cách xử lý xung đột. (B6.2, B8)
- [ ] **[CỨNG] B6.5:** Tách lượng đặt khỏi rủi ro thiếu trước ETA; in-transit không xóa cảnh báo on-hand. Không xem mọi hàng đang về là có sẵn ngay; thiếu ETA phải có nhãn thiếu dữ liệu.
- [ ] **[CỨNG] B6.5:** Projected stock theo ngày xét ETA, reservation/backorder, thứ tự nhận–tiêu thụ; IP cao vẫn có thể thiếu trước ETA.
- [ ] **[CỨNG] B6.6:** Chỉ kết luận ngày cạn trong horizon dự báo đủ thông tin; nếu chưa cạn thì ghi “chưa thấy cạn trong horizon”. Ngoại suy run-rate phải có nhãn, không tạo ngày cạn từ forecast không phủ ngày đó.
- [ ] **[CỨNG] B6.6:** Giữ mục tiêu cảnh báo trước ≥7 ngày và kiểm chứng bằng mô phỏng, không bảo đảm chưa có bằng chứng. Mở/backtest horizon phù hợp, báo ca đủ sớm/muộn/bỏ sót/chưa đủ quan sát; phân biệt hết tồn cuối ngày và thiếu nhu cầu trong ngày.
- [ ] Khi rerun, không tạo đề xuất lặp cho đơn đã chấp nhận; receipt/khuyến nghị cần truy vết trạng thái và idempotency. (D3)

## EOL — đầy đủ các mục cứng B7

EOL không được nêu riêng trong ảnh; vẫn giữ các kịch bản từ PDF/review trong phạm vi mô phỏng. Do chỉ có orders, demo dùng sự kiện và mapping scenario do nhóm khai báo; không đợi log/hợp đồng thật. “Xác nhận” trong scenario là xác nhận cấu hình giả định, không giả danh xác nhận vận hành. Các luật dưới đây ngăn suy luận EOL thật sai từ orders.

- [ ] **[CỨNG] B7.a:** Tách thời điểm ngừng bán, ngừng nhập, hết khả năng kích hoạt và hết hỗ trợ dịch vụ. Suspended phải có đường quay lại active; hết hợp đồng carrier không EOL mọi SKU toàn hệ thống.
- [ ] **[CỨNG] B7.b:** Zero-run, share bằng 0, lỗi tăng hoặc không nạp mã, kể cả cùng xuất hiện, chưa chứng minh ngừng vĩnh viễn. Chỉ xuất “nghi ngừng/gián đoạn”; cần xác nhận vận hành. Rule nhìn lại không tự tạo khả năng cảnh báo trước.
- [ ] **[CỨNG] B7.b:** Pending chưa chắc là lỗi; phân biệt failed+timeout, failed+timeout+pending và non-success theo [DATA_CONTRACT](docs/DATA_CONTRACT.md). Định nghĩa tử/mẫu/cửa sổ/số đơn tối thiểu trước khi áp ngưỡng; ngưỡng đề xuất vẫn cần xác nhận.
- [ ] **[CỨNG] B7.c:** Lịch kiểm tra nhóm ưu tiên thấp không được bỏ lỡ toàn bộ cửa sổ EOL. Review đề xuất chạy rule hằng ngày cho các offering và ưu tiên người xử lý khác nhau; không suy “khó thay thế” từ giá mà thiếu mapping nghiệp vụ.
- [ ] **[CỨNG] B7.d:** Chỉ loại/mask đoạn không còn chào bán theo effective date; không xóa toàn bộ history SKU cũ. Active nhưng stockout không có nghĩa zero nhu cầu. Forecast bán sau EOL có thể bằng 0 theo constraint trong khi nhu cầu tiềm ẩn còn; nói rõ đóng băng model hay output.
- [ ] **[CỨNG] B7.d:** Successor không tự trỏ, không tạo vòng, không nằm trong tập EOL/không active; kiểm tra country, thiết bị và nguồn cung. Không dùng bảng thay thế gốc có self-loop như mapping hợp lệ.
- [ ] Hệ số chuyển đổi/cold-start là **[MỀM]** scenario, không gọi là hệ số đã học; xét nhiều successor, phần giữ được/phần mất và tránh cộng thêm hiệu ứng chuyển đổi đã nằm trong forecast successor. (B7.d)
- [ ] **[CỨNG] B7.e:** Không coi eSIM hủy gần như miễn phí. Mã/quota có thể trả trước/không hoàn/hết hạn; cả hai type cần chính sách hợp đồng. validity_days không phải hạn lưu kho/kích hoạt; có hạn lô thì ưu tiên FEFO thay FIFO thuần túy.
- [ ] **[CỨNG] B7.e:** Chia cho tốc độ bán phải xử lý 0. Không nhân mùa vụ thêm nếu forecast đã có mùa vụ; xét forecast cộng dồn tới hạn cuối bán/kích hoạt. Không khuyến nghị xả sản phẩm khách không còn kích hoạt/sử dụng hợp lệ.
- [ ] **[CỨNG] B7.e:** Phép cộng thời gian nêu trong review phải làm tròn lên 18 thay vì 17 nếu thực sự áp dụng, nhưng không dùng tổng đó làm deadline chuẩn: cam kết NCC chưa xác thực, P90 không bảo vệ đuôi còn lại, activation lag không phải lead time. Max quan sát không bảo đảm grace hợp đồng hoặc thời gian dùng sau kích hoạt.
- [ ] **[CỨNG] B7.f:** Hệ số mùa vụ chưa tái lập không được coi là chắc chắn. Ngưỡng ưu tiên mùa vụ là **[MỀM]** scenario cần sensitivity, không nhân mùa vụ hai lần.
- [ ] **[CỨNG] B7.g:** Có nhánh thông báo muộn, EOL ngay, suspended hồi phục và hủy thông báo. Không mặc định luôn kịp T−17/T−14; last-buy xét ETA/MOQ/ngày cuối bán. T+15 không tự chấm dứt nghĩa vụ với khách.
- [ ] **[CỨNG] B7.h:** Thời gian cảnh báo trước = ngày dừng − ngày phát hiện, không đảo dấu. MAE/bias vẫn tính được sau EOL theo điều kiện mẫu số metric; MAPE gặp vấn đề khi actual=0.
- [ ] **[CỨNG] B7.h:** Không chia số đơn thay thế cho nhu cầu quantity rồi gọi là “giữ khách”. Thống nhất đơn vị; nếu dùng đơn vị sản phẩm, đặt tên tỷ lệ nhu cầu giữ được.
- [ ] Mục tiêu xả tồn/doanh thu/giữ nhu cầu trong B7.h là **[MỀM]**, chưa được dữ liệu chứng minh. Định nghĩa mẫu số/cửa sổ, xử lý doanh thu bằng 0, ghi nhu cầu đối chứng là ước lượng; hệ số scenario không bảo đảm KPI ở mọi ca.
- [ ] **[CỨNG] B7.i:** Bộ cột lifecycle gốc chưa đủ cho carrier, nhiều successor, ngày cuối kích hoạt/dịch vụ, ETA và batch expiry. Lưu người cập nhật, lúc xác nhận, effective dates, provenance; không tự dồn nhu cầu sang carrier cùng region nếu chưa kiểm tra tương thích/năng lực.

## Mô phỏng và các ca kiểm thử bắt buộc

Các ràng buộc từ D3 áp dụng khi triển khai rule, không coi dữ liệu scenario là dữ liệu thật:

- [ ] Policy chỉ thấy thông tin có tại origin; order về theo ETA; bảo toàn tồn kho, nhất quán lost-sales hoặc backorder. So policy trên cùng scenario/demand/randomness; lưu seed nếu sinh ngẫu nhiên.
- [ ] Fill rate tính theo đơn vị đáp ứng/đơn vị yêu cầu. Khai báo giả định một đơn vị quantity bán theo order_date tiêu thụ một đơn vị stock; không tự coi đó là luồng kho thật hoặc mô phỏng là hiệu quả nhu cầu tiềm ẩn thật.
- [ ] Đánh giá cảnh báo tách nhánh đối chứng không đặt thêm ngoài receipt đã có tại origin và nhánh có hành động. Nhập kịp khiến không cạn không tự là false positive.
- [ ] Đếm cảnh báo theo sự kiện, tránh đếm lặp stockout mỗi ngày. Sai số ngày cạn chỉ khi cả hai bên có sự kiện trong cửa sổ; báo trường hợp không cạn/chưa quan sát đủ, không gán ngày cạn giả.
- [ ] Kiểm thử thiếu stock/config; velocity=0 nhưng forecast>0; q_raw=0 có MOQ; stock đúng ngưỡng; hai carrier có ngưỡng/MOQ khác nhau cho kết quả theo đúng config.
- [ ] Kiểm thử hàng về sau ngày cạn; stock đã giữ chỗ; forecast thiếu một ngày; share denominator=0.
- [ ] Kiểm thử EOL một carrier trong khi carrier khác còn bán; successor tự trỏ/vòng; suspended quay lại active; receipt/khuyến nghị chạy lại.

Nguồn: [Review_SIGMA_M2_M3.md](Review_SIGMA_M2_M3.md), mục [phạm vi, A1–A4, B1–B8, D1–D3, E]; cập nhật theo [xác nhận mentor do người dùng cung cấp](docs/PROJECT_OVERVIEW.md), 26/09/2026.

Khi sửa code, luôn đối chiếu lại DECISIONS.md và Review_SIGMA_M2_M3.md trước khi hard-code một giả định mới.

## Quy tắc cập nhật GitHub

- Khi người dùng yêu cầu đẩy cập nhật lên GitHub, thực hiện đủ kiểm tra → commit → push → xác minh; không dừng ở commit local hoặc hỏi lại quyền push đã được cấp.
- Trước khi commit, kiểm tra status, diff, nhánh và remote; chỉ stage các file thuộc phạm vi công việc, giữ nguyên thay đổi không liên quan. Không đưa secret/token, file môi trường hoặc artifact tạm vào commit.
- Chạy `git diff --check` và kiểm tra phù hợp với thay đổi. Với tài liệu, rà tính nhất quán target/KPI và liên kết; với code, chạy kiểm thử liên quan. Không ghi đã chạy model/test khi chưa chạy.
- Viết commit message nêu rõ thay đổi; cập nhật CHANGELOG khi thay đổi target, phạm vi hoặc quy tắc dự án. Fetch trước khi push để kiểm tra chênh lệch với remote; không force-push, reset hay ghi đè công việc của người khác.
- Push lên nhánh/remote đã xác định; nếu remote có cập nhật thì tích hợp và kiểm tra lại trước khi push. Nếu cần nhánh mới, dùng tiền tố `codex/`, trừ khi người dùng chỉ định khác.
- Sau push, xác minh commit trên remote khớp commit local; báo nhánh, commit và liên kết GitHub. Nếu bị chặn bởi quyền truy cập hoặc bảo vệ nhánh, báo đúng trạng thái và nguyên nhân, không tuyên bố đã đẩy thành công.
