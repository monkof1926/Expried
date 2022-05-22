
""" Representing the expiry date of an item """
class Date():

    months_dict = \
        {"1":{"full": "January",    "clipped":"Jan"},
        "2":{ "full": "February",   "clipped":"Feb"},
        "3":{ "full": "March",      "clipped":"Mar"},
        "4":{ "full": "April",      "clipped":"Apr"},
        "5":{ "full": "May",        "clipped":"May"},
        "6":{ "full": "June",       "clipped":"Jun"},
        "7":{ "full": "July",       "clipped":"Jul"},
        "8":{ "full": "August",     "clipped":"Aug"},
        "9":{ "full": "September",  "clipped":"Sep"},
        "10":{"full": "October",    "clipped":"Oct"},
        "11":{"full": "November",   "clipped":"Nov"},
        "12":{"full": "December",   "clipped":"Dec"},
    }

    def __init__(self,day=1,month=1,year=2000):
        self.day = day; self.month = month; self.year = year

    """ For sorting based on date """
    def __lt__(self,other):
        return (self.year,self.month,self.day) < (other.year,other.month,other.day)
    def __gt__(self,other):
        return (self.year,self.month,self.day) > (other.year,other.month,other.day)
    def __eq__(self,other):
        return (self.year,self.month,self.day) == (other.year,other.month,other.day)



    def toString_DMY(self):
        return f"{self.day}/{self.month}-{self.year}"
    
    def toString_MDY(self):
        # if self.day < 10:
        return f"{self.month}/{self.day}-{self.year}"

    def toString_DMY_month(self):
        return f"{self.months_dict[str(self.month)]}"





