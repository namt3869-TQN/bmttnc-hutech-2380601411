class SinhVien:
    def __init__(self, id, name, sex, major, diemTB):
        self._id = id
        self._name = name
        self._sex = sex
        self._major = major
        self._diemTB = diemTB
        self._hocLuc = ""

    def xep_loai(self):
        if self._diemTB >= 8:
            self._hocLuc = "Giỏi"
        elif self._diemTB >= 6.5:
            self._hocLuc = "Khá"
        elif self._diemTB >= 5:
            self._hocLuc = "Trung bình"
        else:
            self._hocLuc = "Yếu"

    def __str__(self):
        return f"ID: {self._id} | Tên: {self._name} | Giới tính: {self._sex} | Ngành: {self._major} | ĐTB: {self._diemTB} | Học lực: {self._hocLuc}"


class QuanLySinhVien:
    def __init__(self):
        self._ds = []
        self._next_id = 1

    def them_sv(self):
        name = input("Tên: ")
        sex = input("Giới tính: ")
        major = input("Chuyên ngành: ")
        diemTB = float(input("Điểm trung bình: "))
        sv = SinhVien(self._next_id, name, sex, major, diemTB)
        sv.xep_loai()
        self._ds.append(sv)
        self._next_id += 1
        print("Thêm thành công!")

    def cap_nhat_sv(self):
        id = int(input("Nhập ID cần cập nhật: "))
        for sv in self._ds:
            if sv._id == id:
                sv._name = input("Tên mới: ")
                sv._sex = input("Giới tính mới: ")
                sv._major = input("Chuyên ngành mới: ")
                sv._diemTB = float(input("Điểm TB mới: "))
                sv.xep_loai()
                print("Cập nhật thành công!")
                return
        print("Không tìm thấy!")

    def xoa_sv(self):
        id = int(input("Nhập ID cần xóa: "))
        for sv in self._ds:
            if sv._id == id:
                self._ds.remove(sv)
                print("Xóa thành công!")
                return
        print("Không tìm thấy!")

    def tim_kiem_sv(self):
        name = input("Nhập tên cần tìm: ")
        for sv in self._ds:
            if name.lower() in sv._name.lower():
                print(sv)

    def sap_xep_diem(self):
        ds_sorted = sorted(self._ds, key=lambda x: x._diemTB, reverse=True)
        for sv in ds_sorted:
            print(sv)

    def sap_xep_nganh(self):
        ds_sorted = sorted(self._ds, key=lambda x: x._major)
        for sv in ds_sorted:
            print(sv)

    def hien_thi_ds(self):
        if not self._ds:
            print("Danh sách trống!")
        for sv in self._ds:
            print(sv)

    def menu(self):
        while True:
            print("\n===== QUẢN LÝ SINH VIÊN =====")
            print("1. Thêm sinh viên")
            print("2. Cập nhật sinh viên")
            print("3. Xóa sinh viên")
            print("4. Tìm kiếm sinh viên")
            print("5. Sắp xếp theo điểm TB")
            print("6. Sắp xếp theo chuyên ngành")
            print("7. Hiển thị danh sách")
            print("0. Thoát")
            choice = input("Chọn: ")
            if choice == "1":
                self.them_sv()
            elif choice == "2":
                self.cap_nhat_sv()
            elif choice == "3":
                self.xoa_sv()
            elif choice == "4":
                self.tim_kiem_sv()
            elif choice == "5":
                self.sap_xep_diem()
            elif choice == "6":
                self.sap_xep_nganh()
            elif choice == "7":
                self.hien_thi_ds()
            elif choice == "0":
                break


qlsv = QuanLySinhVien()
qlsv.menu()