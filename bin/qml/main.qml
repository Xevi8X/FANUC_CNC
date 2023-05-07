import QtQuick
import QtQuick.Window
import QtQuick.Controls
import Qt5Compat.GraphicalEffects
import Qt.labs.platform 1.1
import "controls"

Window {

    id: mainWindow
    width: 1000
    height: 580
    minimumWidth: 800
    minimumHeight: 500
    visible: true
    color: "transparent"
    title: qsTr("Fanuc CNC")


    //Remove title bar
    flags: Qt.Window | Qt.FramelessWindowHint | Qt.WA_TranslucentBackground


    //Properties
    property int windowStatus: 0
    property int windowMargin: 10

    // Text edit properies
    property alias actualPage: stackView.currentItem

    //Internal functions
    QtObject{
        id: internal

        function resizeVisibility(bool){
            resizeLeft.visible = bool
            resizeRight.visible = bool
            resizeBottom.visible = bool
            resizeWindow.visible = bool
        }

        function maximizeRestore(){
            if(windowStatus == 0){
                mainWindow.showMaximized()
                windowStatus = 1
                windowMargin = 0
                internal.resizeVisibility(false)
                btnMaximizeRestore.btnIconSource = "../../images/svg_images/restore_icon.svg"
            } else {
                mainWindow.showNormal()
                windowStatus = 0
                windowMargin = 10
                internal.resizeVisibility(true)
                btnMaximizeRestore.btnIconSource = "../../images/svg_images/maximize_icon.svg"
            }
        }

        function ifMaximizedWindowRestore(){
            if(windowStatus == 1){
                mainWindow.showNormal()
                windowStatus = 0
                windowMargin = 10
                internal.resizeVisibility(true)
                btnMaximizeRestore.btnIconSource = "../../images/svg_images/maximize_icon.svg"
            }
        }

        function restoreMargins(){
            windowStatus = 0
            windowMarin = 10
            internal.resizeVisibility(true)
            btnMaximizeRestore.btnIconSource = "../../images/svg_images/maximize_icon.svg"
        }
    }

    Rectangle {
        id: bg
        color: "#1a5f7a"
        border.color: "#021d48"
        border.width: 10
        anchors.fill: parent
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        
        Rectangle {
            id: appContainer
            color: "#1a5f7a"
            anchors.fill: parent
            anchors.rightMargin: 1
            anchors.leftMargin: 1
            anchors.bottomMargin: 1
            anchors.topMargin: 1
            
            Rectangle {
                id: topBar
                height: 60
                color: "#002b5b"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                anchors.topMargin: 0
                
                ToggleButton {
                    onClicked: animationMenu.running = true
                }
                
                Rectangle {
                    id: topBarDescription
                    y: 28
                    height: 25
                    color: "#159895"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 70
                    anchors.bottomMargin: 0
                    
                    Label {
                        id: labelTopInfo
                        color: "#57c5b6"
                        text: qsTr("Program name")
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        verticalAlignment: Text.AlignVCenter
                        anchors.rightMargin: 300
                        anchors.leftMargin: 10
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                    }
                    
                    Label {
                        id: labelRightInfo
                        color: "#57c5b6"
                        text: qsTr("| Home")
                        anchors.left: labelTopInfo.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        horizontalAlignment: Text.AlignRight
                        verticalAlignment: Text.AlignVCenter
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        anchors.rightMargin: 10
                        anchors.leftMargin: 0
                    }
                }
                
                Rectangle {
                    id: titleBar
                    height: 35
                    color: "transparent"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: 105
                    anchors.leftMargin: 70
                    anchors.topMargin: 0

                    DragHandler {
                        onActiveChanged: if(active) {
                                             mainWindow.startSystemMove()
                                             internal.ifMaximizedWindowRestore()
                                         }
                    }
                    
                    Image {
                        id: iconApp
                        width: 32
                        height: 32
                        fillMode: Image.PreserveAspectFit
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        source: "../images/mel_logo.png"
                        anchors.bottomMargin: 0
                        anchors.leftMargin: 5
                        anchors.topMargin: 0
                    }
                    
                    Label {
                        id: label
                        color: "#57c5b6"
                        text: qsTr("Fanuc CNC")
                        anchors.left: iconApp.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 15
                        anchors.leftMargin: 5
                    }
                }
                
                Row {
                    id: rowBtns
                    width: 105
                    height: 35
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.topMargin: 0
                    anchors.rightMargin: 0
                    
                    TopBarButton {
                        id: btnMinimize
                        onClicked:{
                            mainWindow.showMinimized()
                            internal.restoreMargins()
                        }
                    }

                    TopBarButton {
                        id: btnMaximizeRestore
                        btnIconSource: "../../images/svg_images/maximize_icon.svg"
                        onClicked: internal.maximizeRestore()
                    }

                    TopBarButton {
                        id: btnClose
                        btnColorClicked: "#ff007f"
                        btnIconSource: "../../images/svg_images/close_icon.svg"
                        onClicked: mainWindow.close()
                    }
                }
            }
            
            Rectangle {
                id: content
                color: "transparent"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: topBar.bottom
                anchors.bottom: parent.bottom
                anchors.topMargin: 0
                
                Rectangle {
                    id: leftMenu
                    width: 70
                    color: "#002b5b"
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    clip: true
                    anchors.topMargin: 0
                    anchors.bottomMargin: 0
                    anchors.leftMargin: 0
                    
                    PropertyAnimation{
                        id:animationMenu
                        target: leftMenu
                        property: "width"
                        to: if(leftMenu.width == 70) return 200; else return 70
                        duration: 400
                        easing.type: Easing.InOutQuint
                    }

                    Column {
                        id: columnMenu
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 0
                        anchors.leftMargin: 0
                        anchors.bottomMargin: 90
                        anchors.topMargin: 0
                        
                        LeftMenuBtn {
                            id: btnHome
                            width: leftMenu.width
                            text: qsTr("Home")
                            isActiveMenu: true
                            onClicked: {
                                btnHome.isActiveMenu = true
                                btnSettings.isActiveMenu = false
                                btnRobot.isActiveMenu = false
                                stackView.push("pages/controlPage.qml")
                            }
                        }

                        LeftMenuBtn {
                            id: btnRobot
                            width: leftMenu.width
                            text: qsTr("Hardware")
                            isActiveMenu: false
                            btnIconSource: "../../images/svg_images/robot_icon.svg"
                            onClicked: {
                                btnRobot.isActiveMenu = true
                                btnSettings.isActiveMenu = false
                                btnHome.isActiveMenu = false
                                stackView.push("pages/robotPage.qml")
                            }
                        }

                        LeftMenuBtn {
                            id: btnOpen
                            width: leftMenu.width
                            text: qsTr("Open")
                            isActiveMenu: false
                            btnIconSource: "../../images/svg_images/open_icon.svg"

                            onPressed: {
                                    fileOpen.open()
                                }

                            FileDialog{
                                id: fileOpen
                                fileMode: FileDialog.OpenFile
                                title: "Please choose a NC file"
                                nameFilters: ["NC File (*.NC)"]
                                onAccepted: {
                                    backend.openFile(fileOpen.file)
                                }
                            }
                        }

                        LeftMenuBtn {
                            id: btnSave
                            width: leftMenu.width
                            text: qsTr("Save")
                            btnIconSource: "../../images/svg_images/save_icon.svg"

                            onPressed:{
                                fileSave.open()
                            }

                            FileDialog{
                                id: fileSave
                                fileMode: FileDialog.SaveFile
                                title: "Save NC file"
                                nameFilters: ["NC file (*.NC)"]
                                onAccepted: {
                                    backend.getTextField(actualPage.getText)
                                    backend.writeFile(fileSave.currentFile)
                                }
                            }
                        }
                    }

                    LeftMenuBtn {
                        id: btnSettings
                        width: leftMenu.width
                        text: qsTr("Settings")
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 25
                        btnIconSource: "../../images/svg_images/settings_icon.svg"
                        clip: true
                        onClicked: {
                            btnSettings.isActiveMenu = true
                            btnHome.isActiveMenu = false
                            btnRobot.isActiveMenu = false
                            stackView.push("pages/settingsPage.qml")
                        }

                    }
                }
                
                Rectangle {
                    id: contentPages
                    color: "#00000000"
                    anchors.left: leftMenu.right
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    clip: true
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 25
                    anchors.topMargin: 0

                    StackView {
                        id: stackView
                        anchors.fill: parent
                        Component.onCompleted: stackView.push("pages/controlPage.qml")
                    }
                }
                
                Rectangle {
                    id: rectangle
                    color: "#159895"
                    anchors.left: leftMenu.right
                    anchors.right: parent.right
                    anchors.top: contentPages.bottom
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0
                    
                    Label {
                        id: labelTopInfo1
                        color: "#57c5b6"
                        text: qsTr("Program name")
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        verticalAlignment: Text.AlignVCenter
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        anchors.rightMargin: 30
                        anchors.leftMargin: 10
                    }

                    MouseArea {
                        id: resizeWindow
                        x: 895
                        y: 10
                        width: 25
                        height: 25
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 0
                        anchors.bottomMargin: 0
                        cursorShape: Qt.SizeFDiagCursor

                        DragHandler{
                            target: null
                            onActiveChanged: if(active){
                                                 mainWindow.startSystemResize(Qt.RightEdge | Qt.BottomEdge)
                                             }
                        }

                        Image {
                            id: resizeImage
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            source: "../images/svg_images/resize_icon.svg"
                            anchors.rightMargin: 0
                            anchors.bottomMargin: 0
                            anchors.leftMargin: 5
                            anchors.topMargin: 5
                            sourceSize.height: 16
                            sourceSize.width: 16
                            fillMode: Image.PreserveAspectFit
                            antialiasing: false
                        }

                    }
                }
            }
        }
    }

    DropShadow{
        id: dropShadow
        anchors.fill: bg
        cached: true
        horizontalOffset: 3
        verticalOffset: 3
        radius: 10
        samples: 16
        color: "#80000000"
        smooth: true
        source: bg
    }

    MouseArea {
        id: resizeLeft
        width: 10
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        cursorShape: Qt.SizeHorCursor

        DragHandler{
            target: null
            onActiveChanged: if(active){ mainWindow.startSystemResize(Qt.LeftEdge)}
        }
    }

    MouseArea {
        id: resizeRight
        width: 10
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.topMargin: 10
        anchors.rightMargin: 0
        anchors.bottomMargin: 10
        cursorShape: Qt.SizeHorCursor

        DragHandler{
            target: null
            onActiveChanged: if(active){ mainWindow.startSystemResize(Qt.RightEdge)}
        }
    }

    MouseArea {
        id: resizeBottom
        height: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.bottomMargin: 0
        cursorShape: Qt.SizeVerCursor

        DragHandler{
            target: null
            onActiveChanged: if(active){ mainWindow.startSystemResize(Qt.BottomEdge)}
        }
    }

    Connections{
        target: backend

        function onReadText(text){
            actualPage.setText = text
        }
    }

}


