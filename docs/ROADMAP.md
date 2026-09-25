# Roadmap M2/M3

**[MỀM]** Timeline điều chỉnh từ D2/D3 ngày 25/09/2026 theo [đề bài và xác nhận chỉ có orders](PROJECT_OVERVIEW.md). Các ngày giữ nguyên; công việc chuyển sang activation/tuyến và chủ động dựng scenario M3. Bảng gốc vẫn còn trong review để đối chiếu. Tham số cụ thể cần xác nhận theo [DECISIONS](DECISIONS.md); không chờ nguồn kho/config thật.

M1 đã qua hạn nhưng PDF chưa đủ chứng minh artifact hoàn thành; kiểm kê và bù phần thiếu trong đầu M2, không lập lại M1 như giai đoạn tương lai.

## M2 — 25/09–17/10/2026 (điều chỉnh từ D2)

| Mốc | Việc thực hiện theo thứ tự | Đầu ra/điều kiện hoàn thành |
|---|---|---|
| **25–27/09** | Kiểm kê M1; chốt định nghĩa activation/tuyến, quantity/filter, UTC, cửa sổ đủ quan sát và cách đo KPI gốc. Ghi phạm vi chỉ có orders; cập nhật điểm khác review v0.1. | Data contract v0.2; decision log; danh sách việc chưa chốt và artifact cần bù. |
| **28–30/09** | Pipeline raw → validation → target activation/tuyến; giữ nhánh order-date để tái lập review nếu cần. Lưu checksum/split; chạy naive/moving average và hồ sơ độ thưa trên target mới. | Đối soát theo activation/filter/cửa sổ đã chọn; không lấy kích thước grid v0.1 làm chuẩn target mới; benchmark từng tuyến. |
| **01–05/10** | Feature tại origin, direct h=1…7; thử LightGBM global cho tuyến hoặc cấp con có tổng hợp về tuyến. Poisson là ứng viên, không giả định đúng phân phối; thử calendar riêng. | Predictions validation cùng target/schema baseline; không leakage; ablation calendar. |
| **06–09/10** | Rolling-origin validation; so ứng viên theo đề bài, chọn model/fallback từng tuyến. SBA/TSB nếu chuỗi thưa cần; Prophet giới hạn như đề xuất D2. | Model comparison theo tuyến/horizon, bias và sai số cộng dồn; lựa chọn bằng validation. |
| **10–12/10** | Khóa model/feature/hyperparameter và Top 10 tuyến chọn từ train. Chạy final test trong cửa sổ activation đủ quan sát; thử phân bổ xuống stock item để phát hiện lỗi M3. | Báo cáo KPI MAPE ≤20% đạt/chưa đạt theo cách đo thống nhất, coverage và metric bổ sung; không tuning trên test. |
| **13–15/10** | Đóng gói batch, metadata, rerun, xử lý input thiếu và demo replay lịch sử. Không chờ order mới; không gọi demo là vận hành hiện tại. | Lệnh chạy/config/model artifact; số dòng bằng số series thực tế × horizon được khai báo; không cố định theo grid v0.1. |
| **16–17/10** | Chạy lại từ đầu, rà yêu cầu activation/tuyến và KPI, báo phần chưa đạt/chưa thống nhất; chuẩn bị trình bày và sửa lỗi. | Nộp M2: dữ liệu xử lý, code/config, benchmark/model, kết quả từng tuyến/Top 10, giới hạn và giao diện M3. |

Split rolling-origin và tiêu chí M2 hoàn thành được giữ tại [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md). Bảng này là lịch làm dự án, không phải lịch dữ liệu.

**Lịch dự án khác lịch dữ liệu.** Dataset orders kết thúc trong năm 2025, activation có phần ngoài khoảng order theo [contract](DATA_CONTRACT.md). Demo bằng replay trong cửa sổ đủ quan sát; không lấy lag cũ để gọi là forecast vận hành 2026, không lên kế hoạch xin dữ liệu mới. Split D2 cũ chỉ là tham chiếu, phải rà lại theo activation; không gọi 01–07/01/2026 mặc nhiên là tuần chưa có actual activation.

## M3 — 18/10–07/11/2026 (điều chỉnh từ D3)

| Mốc | Việc thực hiện | Đầu ra/điều kiện hoàn thành |
|---|---|---|
| **18–20/10** | Dựng config scenario kho logic/stock item: stock đầu kỳ, usable/reserved/backorder, L/R/MOQ/ETA, policy và giả định sự kiện trừ kho. Không chờ dữ liệu vận hành. | Contract inventory/config/receipt; snapshot khởi tạo có source/lý do/version/scenario_id; cách sinh và sensitivity rõ. |
| **21–25/10** | Rule engine, phân bổ và projected stock theo ngày; receipt sinh từ đơn đặt và lead time scenario. Mở/backtest horizon theo L+R và mục tiêu cảnh báo trước ≥7 ngày. | Tách qty đặt, rủi ro trước ETA và config thiếu; bảo toàn kho, không tạo đề xuất lặp cho đơn đã chấp nhận. |
| **26–29/10** | Mô phỏng closed-loop trên demand replay với stock/config giả định; so policy cùng scenario và chạy sensitivity. Chạy ba scenario EOL đã nêu trong review với sự kiện giả định có nguồn. | Fill rate, lost units/backorders, stock, lượng nhập và cảnh báo đủ sớm/muộn/bỏ sót; nguồn giả định và giới hạn rõ. |
| **30/10–02/11** | Dashboard dự báo/actual activation/sai số theo tuyến và Top 10; thêm phần tồn kho/cảnh báo có nhãn mô phỏng, giải thích policy và cutoff. | Luồng forecast → allocation → policy → alert trình diễn được; KPI thực nghiệm tách khỏi dữ liệu scenario. |
| **03–05/11** | Kiểm thử biên và rerun/idempotency, chuẩn bị slide/diễn tập theo D3; đối chiếu mục tiêu cảnh báo với kết quả mô phỏng. | Ca kiểm thử quan trọng pass, fallback khi model/config lỗi; báo các scenario chưa đạt và ca chưa đủ quan sát. |
| **06–07/11** | Khoảng đệm sửa lỗi, đóng gói nộp. | Demo, README, config/quy tắc sinh scenario, báo cáo kết quả KPI và hạn chế. |

**Scenario tồn kho [MỀM]:** chọn ma trận minh họa nhỏ như L={1,3,7} ngày; R={1,7}; stock đầu kỳ bằng {3,7,14} ngày nhu cầu trung bình của **train**; MOQ demo cấu hình riêng. Đây là stress test, không phải ước lượng từ order. Khi chưa có lead time thật, không dùng activation lag để điền L. Có thể thêm nhận hàng trễ, nhu cầu tăng và không có hàng về; lưu seed nếu sinh ngẫu nhiên.

Các scenario trên là **đề xuất — cần mentor xác nhận**, không phải L/R/stock đã ước lượng. Thiết kế policy ở [ARCHITECTURE](ARCHITECTURE.md); cách chấm mô phỏng/cảnh báo ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md); ca kiểm thử bắt buộc ở [AGENTS](../AGENTS.md).

## Rủi ro ưu tiên — cập nhật từ bảng E

| Ưu tiên | Rủi ro | Việc cần làm | Xong khi | Giai đoạn áp dụng |
|---|---|---|---|---|
| **P0 — trước feature/model** | Nhầm target order/Region × SKU với activation/tuyến; lệch mẫu đầu/cuối activation | Version hóa target, chốt filter/cửa sổ/tuyến theo câu 1–3 | Tái lập target đúng yêu cầu và phân biệt số liệu v0.1 | M2: trước feature/model |
| **P0 — trước công bố metric** | Leakage đa bước, Top 10 chọn bằng test, MAPE gặp zero | Origin-based features, validation/test riêng, coverage MAPE | Có forecast h=1…7 chỉ từ dữ liệu quá khứ và metric kiểm tra được | M2: trước công bố metric |
| **P0 — trước rule M3** | Khóa bảng thiếu carrier/type; hai công thức lượng nhập | Đồng bộ ERD/schema/output và chốt L/R/IP/policy | Một stock item có một lượng stock và một quyết định truy vết được | M3: trước rule engine |
| **P0 — trước demo cảnh báo** | Zero velocity cho OK giả; transit không ETA; hứa cảnh báo ≥7 ngày | Projected stock theo ngày, thiếu input có trạng thái riêng, horizon thích hợp | Không có ca stock=0/forecast>0 lại “OK” chỉ vì MA7=0 | M3: trước demo cảnh báo |
| **P0 — trước EOL** | Suy luận ngừng vĩnh viễn từ zero; tự chuyển sai carrier/country | Khai báo lifecycle scenario, kiểm tra compatible successor và phần nhu cầu mất | Ngừng một offering không làm dừng/chuyển nhầm hàng khác | M3: EOL scenario |
| **P1 — trong M2** | Độ thưa/Top 10 v0.1 chưa mô tả target activation/tuyến | Đo lại profile/metric tuyến và cấp phân bổ; giữ số liệu cũ làm tham chiếu | Biết chất lượng đúng target và lỗi do allocation | Trong M2, gồm thử phân bổ |
| **P1 — trước nghiệm thu KPI** | Đổi định nghĩa MAPE hoặc bỏ KPI để khớp kết quả | Thống nhất zero coverage/đối tượng/cách tổng hợp, giữ ngưỡng đề bài | Báo đúng đạt/chưa đạt; benchmark A4 được ghi là v0.1 | M2: trước nghiệm thu KPI |
| **P1 — M3** | Diễn giải stock/config giả định như dữ liệu thật | Tự dựng scenario có nguồn và replay; không chờ nguồn vận hành khác | Truy vết giả định và so policy trên cùng scenario | M3: contract/scenario và demo |
| **P1 — EOL** | eSIM coi là miễn phí; grace 15 ngày và báo trước 17 ngày coi như chắc chắn | Cấu hình điều kiện hợp đồng giả định; tách hạn bán/kích hoạt/dịch vụ | Không cam kết hoặc xả hàng vượt quyền phục vụ | M3: EOL scenario |
| **P2 — chỉnh báo cáo** | Cardinality, 730/731, nhãn success, đánh số/tham chiếu chéo | Sửa tập trung sau khi chốt nội dung | Một người khác đọc và tìm đúng công thức/mục tham chiếu | M2/M3: chỉnh báo cáo sau khi chốt nội dung |
| **P2 — sau baseline ổn định** | Feature và hệ số mùa vụ chưa được xác nhận | Lưu định nghĩa, nguồn calendar, ablation; sensitivity hệ số | Có bằng chứng thêm feature tốt hơn baseline, không chỉ trực giác | M2 sau baseline; M3 nếu dùng hệ số EOL |

**Phạm vi hiện hành:** M2 dự báo activation/tuyến và báo KPI gốc; M3 so policy, cảnh báo và dashboard trên scenario do nhóm dựng. Không tự hủy KPI hoặc coi hoàn thành kỹ thuật là đã nghiệm thu; không gắn giả định với hiệu quả kho thật. Giữ các scenario EOL từ PDF/review trong phạm vi mô phỏng.

Nguồn: [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md), mục [B8, D1–D3, E]; timeline/rủi ro được điều chỉnh theo [đề bài và xác nhận của người dùng](PROJECT_OVERVIEW.md), 25/09/2026.
