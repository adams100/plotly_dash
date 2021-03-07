import pandas as pd 
from datetime import datetime, timedelta
from app import *

def date_values(filename):
    with open(r"uploads/" + filename, "r") as f:
        df = pd.read_csv(f)
        df = df.dropna(subset=['Posting date'])
        datetimelist = []
        yearlist = []
        for x in df["Posting date"].tolist():
            try:
                month = x.split("/")[0]
                day = x.split("/")[1]
                year = x.split("/")[2]
            except:
                print("PRINT: ", x)
            datetimelist.append(datetime(int(year), int(month), int(day)))
            yearlist.append(year)

        df["datetimelist"] = datetimelist
        df["datetimelist"].sort_values(ascending=False)
        start_date = df["datetimelist"].min()
        end_date = df["datetimelist"].max()
        xtime = end_date
        datelist = []
        while (xtime >= start_date): 
            datelist.append(str(xtime.year))
            xtime -= timedelta(days=1)

        datedict = {}
        for x in datelist:
            datedict[x] = ""
        yrs = list(datedict.keys())
        yrs.append("Show All Years")
        return yrs


def vendor_list(filename):
    with open(r"uploads/" + filename, "r") as f:
        df = pd.read_csv(f)
        df = df.dropna(subset=['Posting date'])

        # df["Vendor-PO"] = [str(x) + "-" + str(y) for x, y in zip(df['Vendor Name'].tolist(), df["Purchasing Document"].tolist())]
        df = df.sort_values(["Vendor Name"])
        vendors = list(df["Vendor Name"].unique())
        return vendors

def plotdata(filename, vendor, date):
    with open(r"uploads/" + filename, "r") as f:
        df = pd.read_csv(f)
        df = df.dropna(subset=['Posting date'])
        df = df.fillna("0")
        datetimelist = []
        yearlist = []
        for x in df["Posting date"].tolist():
            month = x.split("/")[0]
            day = x.split("/")[1]
            year = x.split("/")[2]
            datetimelist.append(datetime(int(year), int(month), int(day)))
            yearlist.append(year)

        df["datetimelist"] = datetimelist
        df["year"] = yearlist

        df = df.sort_values(['datetimelist'], ascending=True)

        vendor_df = df.loc[df["Vendor Name"] == vendor]

        if date != "Show All Years":
            vendor_date_df = vendor_df.loc[vendor_df["year"] == date]
            maxdate = datetime(int(date)+1, 1, 1) - timedelta(days=1)
        else:
            date = vendor_df['datetimelist'].min().year
            vendor_date_df = vendor_df
            maxdate = vendor_date_df['datetimelist'].max()
        df = None
        df = vendor_date_df.loc[vendor_date_df["Credit Memo"] != "X"]

        mindate = datetime(int(date), 1, 1)
        
        cursor = mindate 
        xticks = []
        while (cursor <= maxdate):
            xticks.append(cursor)
            cursor += timedelta(days=1)

        tick_labels = [datetime.strftime(x, "%m/%d/%Y") if x.day == 1 else "" for x in xticks]
        tick_vals = [datetime.strftime(x, "%m/%d/%Y") for x in xticks]
        x = [datetime.strftime(xx, "%m/%d/%Y") for xx in df["datetimelist"].tolist()]
        

        y = df["Total Amt in Doc Curr"].tolist()
        minval = df["Total Amt in Doc Curr"].min()
        maxval = df["Total Amt in Doc Curr"].max()

        n = [x for x in df["Vendor Name"]]
        opacity = [0.4 for x in df["Vendor Name"]]
        doc_id = df["Document Id"].tolist()
        doc_num = df["Document Number"].tolist()
        ven_num = df["Vendor"].tolist()
        post_date = df["Posting date"].tolist()
        po = df["Purchasing Document"].tolist()
        # ["Document Id", "Document Number", "Vendor", "Vendor Name", "Total Amt in Doc Curr", "Posting date", "Purchasing Document"]
        return {
            "x": x, 
            "y": y, 
            "n": n, 
            "o": opacity, 
            "xtick_vals": tick_vals, 
            "xtick_labels": tick_labels,
            "doc_id": doc_id,
            "doc_num": doc_num,
            "ven_num": ven_num,
            "post_date": post_date,
            "po": po
        }

def filtered_data(filename, vendor, date):
    with open(r"uploads/" + filename, "r") as f:
        df = pd.read_csv(f)
        df = df.dropna(subset=['Posting date'])
        df = df.fillna("0")
        datetimelist = []
        yearlist = []
        for x in df["Posting date"].tolist():
            month = x.split("/")[0]
            day = x.split("/")[1]
            year = x.split("/")[2]
            datetimelist.append(datetime(int(year), int(month), int(day)))
            yearlist.append(year)

        df["datetimelist"] = datetimelist
        df["year"] = yearlist

        df = df.sort_values(['datetimelist'], ascending=True)

        vendordf = df.loc[df["Vendor Name"] == vendor]

        if date != "Show All Years":
            vendor_datedf = vendordf.loc[vendordf["year"] == date]
        else:
            vendor_datedf = vendordf
        

        doc_id = []
        doc_num = []
        ven_num = []
        ven_name = []
        total_amt = []
        post_date = []
        po = []
        data = {}
        doc_id = vendor_datedf["Document Id"].tolist()
        doc_num = vendor_datedf["Document Number"].tolist()
        ven_num = vendor_datedf["Vendor"].tolist()
        ven_name = vendor_datedf["Vendor Name"].tolist()
        total_amt = vendor_datedf["Total Amt in Doc Curr"].tolist()
        post_date = vendor_datedf["Posting date"].tolist()
        po = vendor_datedf["Purchasing Document"].tolist()

        data = {
            "Document_Id": doc_id,
            "Document_Number": doc_num,
            "Vendor_Number": ven_num,
            "Vendor_Name": ven_name,
            "Total_Amount": ["$" + str(x) for x in total_amt],
            "Posting_date": post_date, 
            "Purchasing_Document": po
        }
        return data
