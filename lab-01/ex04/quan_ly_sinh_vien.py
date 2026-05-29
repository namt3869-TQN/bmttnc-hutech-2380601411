from sinh_vien import SinhVien

class QuanLySinhVien:
    def __init__(self):
        self.listSinhVien = []

    def generateId(self):
        maxId = 1
        if len(self.listSinhVien) > 0:
            maxId = self.listSinhVien[0]._id
            for sv in self.listSinhVien:
                if maxId < sv._id:
                    maxId = sv._id
            maxId += 1
        return maxId

    def numSinhVien(self):
        return len(self.listSinhVien)

    def nhapSinhVien(self):
        svId = self.generateId()
        name = input("Nhap ten sinh vien: ")
        sex = input("Nhap gioi tinh sinh vien: ")
        age = int(input("Nhap tuoi sinh vien: "))
        diemTB = float(input("Nhap diem trung binh: "))
        sv = SinhVien(svId, name, sex, age, diemTB)
        self.xetHocLuc(sv)
        self.listSinhVien.append(sv)

    def updateSinhVien(self, ID):
        sv = self.findByID(ID)
        if sv is not None:
            name = input("Nhap ten sinh vien: ")
            sex = input("Nhap gioi tinh sinh vien: ")
            age = int(input("Nhap tuoi sinh vien: "))
            diemTB = float(input("Nhap diem trung binh: "))
            sv._name = name
            sv._sex = sex
            sv._age = age
            sv._diemTB = diemTB
            self.xetHocLuc(sv)
        else:
            print(f"Sinh vien co ID = {ID} khong ton tai.")

    def deleteById(self, ID):
        sv = self.findByID(ID)
        if sv is not None:
            self.listSinhVien.remove(sv)
            return True
        return False

    def findByName(self, keyword):
        listSV = []
        if len(self.listSinhVien) > 0:
            for sv in self.listSinhVien:
                if keyword.upper() in sv._name.upper():
                    listSV.append(sv)
        return listSV

    def findByID(self, ID):
        if len(self.listSinhVien) > 0:
            for sv in self.listSinhVien:
                if sv._id == ID:
                    return sv
        return None

    def xetHocLuc(self, sv: SinhVien):
        if sv._diemTB >= 8:
            sv._hocLuc = "Gioi"
        elif sv._diemTB >= 6.5:
            sv._hocLuc = "Kha"
        elif sv._diemTB >= 5:
            sv._hocLuc = "Trung Binh"
        else:
            sv._hocLuc = "Yeu"

    def sortByPoint(self):
        self.listSinhVien.sort(key=lambda x: x._diemTB, reverse=False)

    def sortByName(self):
        self.listSinhVien.sort(key=lambda x: x._name, reverse=False)

    def showSinhVien(self, listSV):
        print("{:<5} {:<18} {:<10} {:<10} {:<10} {:<10}".format("ID", "Ten", "Gioi Tinh", "Tuoi", "Diem TB", "Hoc Luc"))
        if len(listSV) > 0:
            for sv in listSV:
                print("{:<5} {:<18} {:<10} {:<10} {:<10} {:<10}".format(sv._id, sv._name, sv._sex, sv._age, sv._diemTB, sv._hocLuc))
        print("\n")