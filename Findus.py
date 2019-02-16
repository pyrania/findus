import sys, pickle, datetime
from shutil import copyfile
from PyQt5 import QtCore, QtGui, QtPrintSupport, QtWidgets
from FindusB_UI import Ui_mainWindow
from findus.DeleteDialog import Ui_Dialog


letzterWert = ""
findus = {}
auswahl = []
printer = None
pfad = "/Users/andi/Library/Application Support/hippo/"


class MyDelegate(QtWidgets.QItemDelegate):
    def createEditor(self, parent, option, index):
        if not index.parent().data() or index.column() == 0:
            return super(MyDelegate, self).createEditor(parent, option, index)
        return None


def mainInit():
    global app, window, ui
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(window)

    ui.baum.setColumnWidth(0, 210)
    ui.baum.setColumnWidth(1, 140)
    ui.baum.setColumnWidth(2, 35)
    ui.baum.setColumnHidden(3, True)
    ui.baum.sortItems(0, QtCore.Qt.AscendingOrder)
    ui.baum.setAttribute(QtCore.Qt.WA_MacShowFocusRect, False)
    ui.suchText.setAttribute(QtCore.Qt.WA_MacShowFocusRect, False)

    delegate = MyDelegate()
    ui.baum.setItemDelegate(delegate)


def mainConnect():
    global ui
    ui.baum.currentItemChanged.connect(onCurrentItemChanged)
    ui.baum.itemChanged.connect(onChangedItem)
    ui.suchText.textEdited.connect(onSearch)

    ui.aNeuer_Content.triggered.connect(onAddContent)
    ui.aNeuer_Container.triggered.connect(onAddContainer)
    ui.aWiderrufen.triggered.connect(onUnDo)
    ui.aLoeschen.triggered.connect(onDeleteItem)
    ui.aDrucken.triggered.connect(onPrint)


def mainStart():
    global app, window, findus
    dataLoad("findusB.dat")
    dataView(findus)
    window.show()
    sys.exit(app.exec_())


def addContainer(Bezeichnung, Raum , Platz, UID):
    global ui
    containerItem = QtWidgets.QTreeWidgetItem((Bezeichnung, Raum, Platz, UID))
    containerItem.setFlags(containerItem.flags() | QtCore.Qt.ItemIsEditable)
    ui.baum.addTopLevelItem(containerItem)
    return containerItem


def addContent(content, containerItem):
    contentItem = QtWidgets.QTreeWidgetItem((content, "", "", ""))
    contentItem.setFlags(contentItem.flags() | QtCore.Qt.ItemIsEditable)
    containerItem.addChild(contentItem)
    return contentItem


def deleteDialog():
    global delConfirm, delDialog
    delConfirm = False
    delDialog = QtWidgets.QDialog()
    u = Ui_Dialog()
    u.setupUi(delDialog)

    u.bOK.clicked.connect(delAccept)
    u.bCancel.clicked.connect(delReject)
    delDialog.exec_()
    return delConfirm


def delAccept():
    global delConfirm, delDialog
    delConfirm = True
    delDialog.close()


def delReject():
    global delConfirm
    delConfirm = False
    delDialog.close()


def dataLoad(datei):
    global findus, pfad
    with open(pfad + datei, "rb") as file:
        findus = pickle.load(file)
    dataView(findus)


def dataSave():
    global findus
    copyfile(pfad + "findusB.dat", pfad + "findusB.bak")
    with open(pfad + "findusB.dat", "wb") as datei:
        pickle.dump(findus,datei)


def dataView(dictionary):
    global ui
    ui.baum.clear()
    for container in dictionary.keys():
        containerItem = addContainer(dictionary[container][0], dictionary[container][1], dictionary[container][2], container)
        for content in dictionary[container][3]:
            addContent(content, containerItem)


def paintLabels():
    global auswahl, printer
    painter = QtGui.QPainter()
    painter.begin(printer)

    i = 0
    for container in auswahl:

        painter.setFont(QtGui.QFont("Stencil", 96))
        painter.drawText(QtCore.QRectF(xy(9 + (i % 2) * 105), xy(7 + (i // 2) * 35), xy(40), xy(25)),
                         QtCore.Qt.AlignRight | QtCore.Qt.AlignTop, container[0])

        painter.setFont(QtGui.QFont("Verdana", 12, QtGui.QFont.Bold))
        painter.drawText(QtCore.QRectF(xy(55 + (i % 2) * 105), xy(10 + (i // 2) * 35), xy(45), xy(7)),
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop, container[1])

        contents = len(container[2])
        for j in range(1, min(contents, 3) + 1):
            painter.setFont(QtGui.QFont("Verdana", 12, QtGui.QFont.Normal))
            painter.drawText(QtCore.QRectF(xy(55 + (i % 2) * 105), xy(10 + (i // 2) * 35 + j * 7), xy(45), xy(7)),
                             QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                             container[2][j - 1] + (" …" if j == 3 and contents > 3 else ""))

        i += 1
        if i == 16:
            printer.newPage()
            i = 0

    painter.end()


def xy(mm):
    return round(mm * 11.811, 0)


def onAddContainer():
    global ui, findus
    testID = 0
    nextUID = format(testID, '03d')
    while nextUID in findus.keys():
        testID += 1
        nextUID = format(testID, '03d')
    findus[nextUID] = ["NEU", "Raum", "99",[]]
    dataSave()
    newContainer = addContainer("NEU", "Raum", "99", nextUID)
    ui.baum.clearSelection()
    ui.baum.setCurrentItem(newContainer)


def onAddContent():
    global ui, findus
    if ui.baum.selectedItems():
        selectedItem = ui.baum.selectedItems()[0]
        if selectedItem.parent():
            containerItem = selectedItem.parent()
        else:
            containerItem = selectedItem
        newContent = addContent("NEU", containerItem)
        findus[containerItem.data(3,0)][3].append("NEU")
        dataSave()
        ui.baum.clearSelection()
        ui.baum.setCurrentItem(newContent)
    else:
        onAddContainer()


def onChangedItem(itemChanged, spalte):
    global findus, letzterWert
    if itemChanged.parent():
        neuerWert = itemChanged.data(0, 0)
        UID = itemChanged.parent().data(3, 0)
        findus[UID][3].remove(letzterWert)
        findus[UID][3].append(neuerWert)
    else:
        neuerWert = itemChanged.data(spalte,0)
        UID = itemChanged.data(3,0)
        findus[UID][spalte] = neuerWert
    dataSave()


def onCurrentItemChanged(neu, alt):
    global letzterWert
    if neu:
        letzterWert = neu.data(0,0)


def onDeleteItem():
    global ui, findus
    selectedItems = ui.baum.selectedItems()
    if selectedItems:
        if deleteDialog():
            for item in selectedItems:
                if item.parent():
                    try:
                        parent = item.parent()
                        UID = parent.data(3,0)
                        findus[UID][3].remove(item.data(0,0))
                        dataSave()
                        parent.removeChild(item)
                    except:
                        pass
                else:
                    UID = item.data(3,0)
                    findus.pop(UID)
                    dataSave()
                    ui.baum.invisibleRootItem().removeChild(item)


def onPrint():
    global printer, auswahl, ui

    auswahl = []
    selectedItems = ui.baum.selectedItems()
    if selectedItems:
        for item in selectedItems:
            if not item.parent():
                UID = item.data(3, 0)
            else:
                UID = item.parent().data(3, 0)
            if [findus[UID][2], findus[UID][0], findus[UID][3]] not in auswahl:
                auswahl.append([findus[UID][2], findus[UID][0], findus[UID][3]])
    else:
        iterator = QtWidgets.QTreeWidgetItemIterator(ui.baum)
        while iterator.value():
            item = iterator.value()
            if not item.parent():
                UID = item.data(3, 0)
            else:
                UID = item.parent().data(3, 0)
            if [findus[UID][2], findus[UID][0], findus[UID][3]] not in auswahl:
                auswahl.append([findus[UID][2], findus[UID][0], findus[UID][3]])
            iterator += 1

    auswahl.sort(key=lambda a:a[0])

    printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
    printer.setFullPage(True)
    printer.setPageMargins(0.0, 0.0, 0.0, 0.0, printer.DevicePixel)
    printer.setDoubleSidedPrinting(False)
    printer.setDocName("fin{:%Y%m%d%H%M%S}".format(datetime.datetime.now()))

    preview = QtPrintSupport.QPrintPreviewDialog(printer)
    preview.setWindowState(QtCore.Qt.WindowMaximized)
    preview.paintRequested.connect(paintLabels)
    preview.exec()


def onSearch(gesucht):
    global ui, findus
    gefunden = {}
    if len(gesucht) >= 2:
        for container in findus:
            if ((gesucht.lower() in findus[container][0].lower()) or
                    (gesucht.lower() in findus[container][1].lower()) or (gesucht in findus[container][2])):
                gefunden[container] = (findus[container][0], findus[container][1], findus[container][2],[])
            for content in findus[container][3]:
                if gesucht.lower() in content.lower():
                    if container not in gefunden.keys():
                        gefunden[container] = (findus[container][0], findus[container][1], findus[container][2], [])
                    gefunden[container][3].append(content)
        dataView(gefunden)
        ui.baum.expandAll()
    elif gesucht == "":
        dataView(findus)


def onUnDo():
    global findus
    dataLoad("findusB.bak")
    dataSave()
    dataView(findus)


mainInit()
mainConnect()
mainStart()

