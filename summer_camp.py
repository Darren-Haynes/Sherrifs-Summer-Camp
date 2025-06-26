class SummerCamp:
    def __init__(self) -> None:
        # all the childrens 1st, 2nd and 3rd land and water choices
        self.data = self.instantiate_data()

    def instantiate_data(self):
        data = {}
        with open("Data/orig-data.txt", "r") as file:
            for line in file.readlines():
                sep = line.strip().split(",")
                data[sep[0]] = sep[1:]
        return data
