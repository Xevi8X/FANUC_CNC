import QtQuick
import QtQuick.Controls
import "../controls"
import QtQuick.Layouts 6.3

Item {
    Rectangle {
        id: rectangle
        color: "#159895"
        anchors.fill: parent
        
        Rectangle {
            id: rectangleTop
            height: 69
            color: "#1a5f7a"
            radius: 10
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: 50
            anchors.leftMargin: 50
            anchors.topMargin: 40

            GridLayout {
                anchors.fill: parent
                rows: 1
                columns: 3
                anchors.rightMargin: 10
                anchors.leftMargin: 10

                CustomTextField {
                    id: textField
                    placeholderText: "Type your name"
                    Layout.fillWidth: true
                    Keys.onReturnPressed: {
                        backend.welcomeText(textField.text)
                    }
                }

                CustomButton {
                    id: btnChangeName
                    text: "Change Name"
                    Layout.maximumWidth: 200
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    Layout.preferredWidth: 250
                    onClicked: {
                        backend.welcomeText(textField.text)
                    }

                }

                Switch {
                    id: switchHome
                    text: qsTr("Switch")
                    checked: true
                    Layout.preferredHeight: 40
                    Layout.preferredWidth: 68

                    // Change show/hide state
                    onToggled: {
                        backend.showHideRectangle(switchHome.checked)
                    }

                }
            }
        }
        
        Rectangle {
            id: rectangleContent
            color: "#002b5b"
            radius: 10
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: rectangleTop.bottom
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 40
            anchors.topMargin: 10
            anchors.rightMargin: 50
            anchors.leftMargin: 50
            
            Label {
                id: labelTextName
                y: 8
                height: 25
                color: "#5c667d"
                text: qsTr("Welcome")
                anchors.left: parent.left
                anchors.right: parent.right
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 14
                anchors.rightMargin: 10
                anchors.leftMargin: 10
            }
            
            Label {
                id: labelDate
                y: 31
                height: 25
                color: "#55aaff"
                text: qsTr("Date")
                anchors.left: parent.left
                anchors.right: parent.right
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 12
                anchors.rightMargin: 10
                anchors.leftMargin: 10
            }

            ScrollView {
                id: scrollView
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: labelDate.bottom
                anchors.bottom: parent.bottom
                clip: true
                anchors.topMargin: 10
                anchors.bottomMargin: 10
                anchors.leftMargin: 10
                anchors.rightMargin: 10

                Text {
                    id: textHome
                    color: "#a9b2c8"
                    text: "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">GNU GENERAL PUBLIC LICENSE</span></p>\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Version 3, 29 June 2007</p>\n<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Copyright (c) 2020 <span style=\" font-weight:600;\">Wanderson M. Pimenta</span></p>\n<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p>\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#55aaff;\">Attention</span>: this project was created with the Open Souce tools from Qt Company,</p>\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">this project can be used for studies or personal non-commercial projects. </p>\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">If you are going to use it for </span><span style=\" font-weight:600; color:#55aaff;\">commercial use</span><span style=\" font-weight:600;\">, you need to purchase a license at &quot;https://www.qt.io&quot;.</span></p></body></html>"
                    anchors.fill: parent
                    font.pixelSize: 12
                    textFormat: Text.RichText
                }
            }
        }

        Connections{
            target: backend

            function onSetName(name){
                labelTextName.text = name
            }

            function onPrintTime(time){
                labelDate.text = time
            }

            function onIsVisible(isVisible){
                rectangleContent.visible = isVisible
            }
        }
    }
    
}
