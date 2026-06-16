# legal-admin

## Purpose

Skill `legal-admin` dùng để tiếp nhận văn bản hành chính và tạo metadata quản lý tài liệu. Mục tiêu là giúp người dùng phân loại, theo dõi, giao việc và tìm lại văn bản nhanh chóng.

Skill này không dùng để OCR toàn văn, không bóc bảng/phụ lục dài, không phân tích pháp lý sâu, trừ khi người dùng yêu cầu riêng.

## Default Behavior

Khi nhận một file PDF công văn, thông báo, quyết định, tờ trình hoặc văn bản hành chính tương tự, chỉ trích xuất thông tin cốt lõi phục vụ quản lý tài liệu.

## Processing Rules

1. Đọc phần văn bản chính từ trang đầu cho đến khi gặp trang có chữ ký, con dấu, nơi nhận hoặc dấu hiệu kết thúc văn bản chính.
2. Nếu trong phần văn bản chính có bảng biểu, danh sách, danh mục hoặc biểu mẫu, chỉ đọc phần tiêu đề/dòng mô tả liên quan đến metadata; không bóc từng dòng chi tiết.
3. Nếu sau phần văn bản chính có phụ lục, bảng biểu, danh sách dài, danh mục, biểu mẫu hoặc nhiều trang dạng bảng, hãy bỏ qua phần đó.
4. Không quay lại chỉ lấy metadata trang 1 nếu văn bản chính còn tiếp ở các trang sau.
5. Không bóc chi tiết phụ lục, bảng biểu, danh sách dài trừ khi người dùng yêu cầu riêng.
6. Nếu trang 1 đã có đủ metadata, nội dung chính, nơi nhận và chữ ký/con dấu thì chỉ cần dùng trang 1.
7. Nếu trang 1 chưa có chữ ký/con dấu/nơi nhận hoặc chưa có dấu hiệu kết thúc văn bản chính, hãy đọc tiếp các trang sau cho đến khi gặp các dấu hiệu này rồi dừng.
8. Khi phát hiện các trang sau là phụ lục/bảng/danh sách dài, chỉ ghi nhận ngầm để hiểu cấu trúc văn bản; không trích xuất chi tiết vào JSON v1.
9. Ưu tiên tốc độ: không render/đọc toàn bộ PDF nếu đã xác định đủ 7 field schema v1 và đã gặp dấu hiệu kết thúc phần văn bản chính.
10. Nếu text extraction bị rác hoặc thiếu metadata chính, dùng vision trên các trang cần đọc.
11. Ưu tiên ảnh độ phân giải vừa đủ; không render ảnh quá nặng nếu không cần.
12. Không dùng internet, `web_search`, `web_fetch` hoặc crawl.
13. Không in base64.
14. Không tạo script mới nếu người dùng chưa yêu cầu.
15. Không nhắc hoặc tạo file `quy_trinh_xu_ly_ho_so.py`.
16. Nếu không thấy thông tin, ghi `"N/A"`, không suy diễn.
17. Chỉ trả JSON theo schema v1.

## Required Output Schema

Chỉ trả JSON theo schema sau, không giải thích dài dòng:

```json
{
 "ten_file": "",
 "co_quan_ban_hanh": "",
 "so_hieu": "",
 "ngay_ban_hanh": "",
 "van_de_chinh": "",
 "bo_phan_can_xu_ly": [""],
 "deadline": ""
}
```

### Field Meaning
- **ten_file**: tên file PDF gốc được nhận từ người dùng.
- **co_quan_ban_hanh**: cơ quan hoặc tổ chức ban hành văn bản.
- **so_hieu**: số hiệu văn bản nếu xác định được.
- **ngay_ban_hanh**: ngày ban hành văn bản; nếu không xác định được thì ghi "N/A".
- **van_de_chinh**: 1 câu ngắn mô tả văn bản đang nói hoặc xử lý vấn đề gì, không tóm tắt dài.
- **bo_phan_can_xu_ly**: đơn vị/cá nhân được giao việc, cần thực hiện hành động, hoặc thuộc nhóm nơi nhận cần biết để xử lý hồ sơ; nếu văn bản chỉ để lưu tham khảo thì ghi ["N/A"].
- **deadline**: thời hạn xử lý, trả lời hoặc thời hạn thực hiện được nêu rõ trong văn bản; nếu không có thì ghi "N/A".

## Parser

Script xử lý hiện tại nằm tại:
`/root/.openclaw/workspace/skills/legal-admin/scripts/parser.py`
Không sửa script này trừ khi người dùng yêu cầu rõ ràng.
