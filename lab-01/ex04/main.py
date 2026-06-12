from quan_ly_sinh_vien import QuanLySinhVien

qlsv = QuanLySinhVien()
while True:
    print("--- QUAN LY SINH VIEN ---")
    print("1. Them sinh vien.")
    print("2. Cap nhat thong tin sinh vien boi ID.")
    print("3. Xoa sinh vien boi ID.")
    print("4. Tim kiem sinh vien theo ten.")
    print("5. Sap xep sinh vien theo diem trung binh.")
    print("6. Sap xep sinh vien theo ten.")
    print("7. Hien thi danh sach sinh vien.")
    print("0. Thoat chuong trinh.")
    
    key = input("Nhap lua chon cua ban: ")
    if key == '1':
        print("\n1. Them sinh vien.")
        qlsv.nhapSinhVien()
        print("\nThem sinh vien thanh cong!")
    elif key == '2':
        print("\n2. Cap nhat thong tin sinh vien boi ID.")
        ID = int(input("Nhap ID sinh vien can cap nhat: "))
        qlsv.updateSinhVien(ID)
    elif key == '3':
        print("\n3. Xoa sinh vien boi ID.")
        ID = int(input("Nhap ID sinh vien can xoa: "))
        if qlsv.deleteById(ID):
            print(f"\nXoa sinh vien co ID = {ID} thanh cong!")
        else:
            print(f"\nSinh vien co ID = {ID} khong ton tai.")
    elif key == '4':
        print("\n4. Tim kiem sinh vien theo ten.")
        name = input("Nhap ten sinh vien can tim: ")
        searchResult = qlsv.findByName(name)
        qlsv.showSinhVien(searchResult)
    elif key == '5':
        print("\n5. Sap xep sinh vien theo diem trung binh.")
        qlsv.sortByPoint()
        qlsv.showSinhVien(qlsv.listSinhVien)
    elif key == '6':
        print("\n6. Sap xep sinh vien theo ten.")
        qlsv.sortByName()
        qlsv.showSinhVien(qlsv.listSinhVien)
    elif key == '7':
        print("\n7. Hien thi danh sach sinh vien.")
        qlsv.showSinhVien(qlsv.listSinhVien)
    elif key == '0':
        print("\nBan da thoat chuong trinh!")
        break
    else:
        print("\nLua chon khong hop le! Vui loy nhap lai.")