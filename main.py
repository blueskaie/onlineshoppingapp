from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from urllib.request import urlopen
from bs4 import BeautifulSoup
import webbrowser

archiveds = [
    {'category':'alumni', 'filename':'alumni.html', 'url':'http://www.beaversportswear.com/alumni'},
    {'category':'gifts', 'filename':'gifts.html','url':'http://www.beaversportswear.com/gifts'},
    {'category':'hats', 'filename':'hats.html','url':'http://www.beaversportswear.com/hats'},
]

onlines = [
    {'category':'Longines watches', 'url':'https://www.one-prices.com/longines/'},
    {'category':'Seiko watches', 'url':'https://www.one-prices.com/seiko/'},
    {'category':'Alpina watches', 'url':'https://www.one-prices.com/alpina/'},
    # {'category':'Computer accessories', 'url':'https://feed.zazzle.com/rss?qs=computer-accessories'},
    # {'category':'alumni', 'url':'alumni.html'},
]

onlineproducts = []
archivedproducts = []

def get_element_text(element=''):
    if element is None:
        return "None"
    else:
        return element.getText() 

class shoppingboard:
    'this is mainboard for online shopping'
    window = None # this is main board
    currentsubwindow = None # this is current board
    selectedStore = None # this will be 'OnlineStore' or 'ArchivedStore'
    cart = []

    def __init__(self):
        super().__init__()
        self.initmainUI()
        

    def initmainUI(self):
        self.window = Tk()
        self.window.configure(background='#6DC6D8')
        self.window.title("Online Shopping App")
        self.window.geometry("704x650")
        
        title = Label(self.window, text="Welcome to the Online Shopper!",justify=CENTER, fg="BLUE", bg='#6DC6D8', font=("Courier", 28))
        title.grid(column = 0, row = 0)

        img = ImageTk.PhotoImage(Image.open("banner.jpg"))
        banner = Label(self.window, image = img)
        banner.grid(column = 0, row = 1)
        
        labelframe = LabelFrame(self.window, text = "Archive Sales", bg='#6DC6D8', fg="BLUE", font=("Courier", 16))
        labelframe.place(x=30, y=300)
        self.var = IntVar()
        i = 0
        for archived in archiveds:
            R1 = Radiobutton(labelframe, text = archived['category'], variable = self.var, bg='#6DC6D8', value = i, justify=CENTER, fg="BLUE", font=("Courier", 12),command=self.archivedProductsWindow)
            R1.pack(anchor = W)
            i += 1

        labelframe = LabelFrame(self.window, text = "Online Sales", bg='#6DC6D8', fg="BLUE", font=("Courier", 16))
        labelframe.place(x=480, y=300)
        # var = IntVar()
        
        i = 0
        for online in onlines:
            R1 = Radiobutton(labelframe, text = online['category'], variable = self.var, bg='#6DC6D8', value = i, justify=CENTER, fg="BLUE", font=("Courier", 12),command=self.onlineProductsWindow)
            R1.pack(anchor = W)
            i += 1

        itemlabel = Label(self.window, text="Select item number",justify=CENTER, bg='#6DC6D8', fg="BLUE", font=("Courier", 12))
        itemlabel.place(x=270, y=420)
        self.itemnumber = Spinbox(self.window, width=2,from_=1, to=10, fg="BLUE", font=("Courier", 16))
        self.itemnumber.place(x=250, y=450)

        self.addButton = Button(self.window, text = "Add to cart",state=DISABLED, bg='#6DC6D8', fg="BLUE", font=("Courier", 16), command=self.addCart)
        self.addButton.place(x=300, y=445)

        linelabel = Label(self.window, text="--------------------------------------------------------------",justify=CENTER, bg='#6DC6D8', fg="BLUE", font=("Courier", 12))
        linelabel.place(x=30, y=490)
        
        self.printButton = Button(self.window, text = "Print invoice",state=DISABLED, bg='#6DC6D8', fg="BLUE", font=("Courier", 16), command=self.printInvoice)
        self.printButton.place(x=260, y=520)

        self.stateText = StringVar()
        self.stateEntry = Entry(self.window,textvariable=self.stateText,state=DISABLED, bd=2, justify=LEFT, bg="WHITE", fg="BLUE", font=("Courier", 12), width=69)
        self.stateText.set("Status: Choose a sales category...")
        # statelabel = Label(self.window, text="State:",justify=LEFT, bg="WHITE", fg="BLUE", font=("Courier", 12), width=70, bd=5)
        # statelabel = Label(self.window, text="State: ",justify=CENTER, bd=2, width=650, fg="BLUE", font=("Courier", 12))
        self.stateEntry.place(x=2, y=580)

        self.window.mainloop()

    def printInvoice(self):
        f = open('invocie.html','w')
        message = """<html>
        <head>
            <title>Invocie</title>
            <style>
                body {
                    margin: 0 auto;
                    width: 70%;
                }
                h1, h2, p, h3{
                    text-align:center
                }
                .product {
                    border: 1px solid black;
                    margin-bottom:1px;
                }
            </style>
        </head>
        <body><h1>Online Shopper Trading Co. Invoice</h1>
        """
        total = 0
        for product in self.cart:
            total += float(product['price'])
            message += "<div class='product'>"
            message += "<h3>" + product['name'] + "</h3>"
            message += "<p><img src='"+ product['image'] +"'></p>"
            message += "<p> Our price:" + product['price'] + "</p>"
            message += "</div>"
        message += "<h2>Total for the above purchases:<br>$"+str(total) +"</h2>"
        message += "<h7>Archive Store:</h7>"
        message += "<ul>"
        for archive in archiveds:
            message += "<li><a href='"+archive['url']+"'>"+archive['url']+"</a></li>"
        message += "</ul>"
        message += "<h7>Online Store:</h7>"
        message += "<ul>"
        for online in onlines:
            message += "<li><a href='"+online['url']+"'>"+online['url']+"</a></li>"
        message += "</ul>"
        message += """</body></html>"""
        f.write(message)
        f.close()
        self.cart = []
        self.printButton.config(state="disable")
        self.stateText.set("Status: Printed Invoice")
        webbrowser.open_new_tab('invocie.html')

    def addCart(self):
        index = int(self.itemnumber.get())
        if self.selectedStore == "ArchivedStore":
            product = archivedproducts[index-1]
        elif self.selectedStore == "OnlineStore":
            product = onlineproducts[index-1]
        else:
            return
        product['store'] = self.selectedStore
        self.cart.append(product)
        self.printButton.config(state="normal")
        self.stateText.set("Status: Item "+str(index)+" from "+self.selectedStore+" added to cart...")

    def archivedProductsWindow(self):
        self.addButton.config(state="normal")
        self.selectedStore = "ArchivedStore"
        index = self.var.get()
        if self.currentsubwindow:
            self.currentsubwindow.destroy()
        self.currentsubwindow = Toplevel(background='#6DC6D8')
        self.currentsubwindow.wm_title(archiveds[index]['category'])
        self.currentsubwindow.wm_geometry("600x600+100+100")
        l = Label(self.currentsubwindow, text=archiveds[index]['category'],bg='#6DC6D8', fg="BLUE", font=("Courier", 16))
        l.pack()

        TextArea = Text(self.currentsubwindow, bg='blue', fg="white")
        # TextArea.insert(INSERT, "Hello\nGood morning")
        TextArea.insert(INSERT, self.parseArchivedFile(archiveds[index]['filename']))
        TextArea.pack(expand=YES, fill=BOTH)
        self.stateText.set("Status: Choose a item form "+archiveds[index]['category']+" ...")
    
    def onlineProductsWindow(self):
        self.addButton.config(state="normal")
        self.selectedStore = "OnlineStore"
        index = self.var.get()
        if self.currentsubwindow:
            self.currentsubwindow.destroy()
        self.currentsubwindow = Toplevel(background='#6DC6D8')
        self.currentsubwindow.wm_title(onlines[index]['category'])
        self.currentsubwindow.wm_geometry("600x600+100+100")
        l = Label(self.currentsubwindow, text=onlines[index]['category'],bg='#6DC6D8', fg="BLUE", font=("Courier", 16))
        l.pack()

        TextArea = Text(self.currentsubwindow, bg='blue', fg="white")
        # TextArea.insert(INSERT, "Hello\nGood morning")
        TextArea.insert(INSERT, self.parseOnlineUrl(onlines[index]['url']))
        TextArea.pack(expand=YES, fill=BOTH)
        self.stateText.set("Status: Choose a item form "+onlines[index]['category']+" ...")

    def parseOnlineUrl(self, url):
        result = ""
        web_page = urlopen(url)
        page = BeautifulSoup(web_page, "lxml")
        product_eles = page.find("div",{"class":"index_right_txt"}).findAll("ul")
        i = 1
        for product_ele in product_eles:
            name = product_ele.find("li",{"class":"Writing"}).find("a")
            price = product_ele.find("li", {"class":"price"})
            image = product_ele.find("li", {"class":"index_pic"}).find("img")
            product = {}
            product['name'] = get_element_text(element=name)
            price = get_element_text(element=price)
            price = price.replace("Price: $","")
            product['price'] = price
            product['image'] = "https://www.one-prices.com"+image['src']
            # onlineproducts[index].append(product)
            onlineproducts.append(product)
            result = result + str(i) + ":  " + product['name'] + "(" + product['price'] + ")" + "\n"
            i += 1
        result += "------------------------------------------------------------------\n"
        result +=url
        return result

    def parseArchivedFile(self, filename):
        result = ""
        file = open('archived/'+filename)
        content = file.read()
        page = BeautifulSoup(content, "lxml")
        product_eles = page.find("div",{"id":"CategoryContent"}).find("ul",{"class":"ProductList"}).findAll("li")
        i = 1
        for product_ele in product_eles:
            name = product_ele.find("div",{"class":"ProductDetails"}).find("a")
            price = product_ele.find("div", {"class":"ProductPriceRating"}).find("em")
            image = product_ele.find("div", {"class":"ProductImage QuickView"}).find("img")
            product = {}
            product['name'] = get_element_text(element=name)
            price = get_element_text(element=price)
            price = price.replace("$","")
            product['price'] = price
            product['image'] = image['src']
            # onlineproducts[index].append(product)
            archivedproducts.append(product)
            result = result + str(i) + ":  " + product['name'] + "(" + product['price'] + ")" + "\n"
            i += 1
        result += "------------------------------------------------------------------\n"
        result +=filename
        return result

def main():
    s = shoppingboard()
    
if __name__ == "__main__":
    main()