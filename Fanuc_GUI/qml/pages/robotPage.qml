import QtQuick
import QtQuick.Controls
import "../controls"
import QtQuick.Layouts 6.3

Item {
    id: item1
    property alias rectangleTop: rectangleTop
    property string currPort: "Port: Non connected"

    Rectangle {
        id: rectangleTop
        height: 69
        color: "#17191e"
        radius: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 50
        anchors.leftMargin: 50
        anchors.topMargin: 60

        GridLayout {
            anchors.fill: parent
            anchors.topMargin: 0
            rows: 1
            columns: 3
            anchors.rightMargin: 10
            anchors.leftMargin: 10

            CustomTextField {
                id: textField
                placeholderText: "Type robot IP adress"
                Layout.fillWidth: true
                Keys.onReturnPressed: {
                    backend.addressIP(textField.text)
                }
            }

            CustomButton {
                text: "Connect"
                Layout.maximumWidth: 200
                Layout.fillWidth: true
                Layout.preferredHeight: 40
                Layout.preferredWidth: 250
                onClicked: {
                    backend.addressIP(textField.text)
                }

            }
        }
    }

    Label {
        id: labelConnection
        height: 25
        color: "#17191e"
        text: qsTr("Connection")
        anchors.verticalCenter: switchConnect.verticalCenter
        anchors.left: rectangleTop.left
        anchors.bottom: rectangleTop.top
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        anchors.verticalCenterOffset: -2
        anchors.bottomMargin: 5
        font.pointSize: 14
        anchors.rightMargin: 10
        anchors.leftMargin: 3
    }

    Switch {
        id: switchConnect
        font.pointSize: 12
        text: qsTr("Hide")
        anchors.left: labelConnection.right
        anchors.bottom: rectangleTop.top
        anchors.leftMargin: 10
        anchors.bottomMargin: 5

        // Change show/hide state
        onToggled: {
            backend.showHideRectangle(switchConnect.checked)
            switchConnect: checked ? switchConnect.text = qsTr("Hide") : switchConnect.text = qsTr("Show")
        }

        indicator: Rectangle {
            implicitWidth: 48
            implicitHeight: 26
            x: switchConnect.leftPadding
            y: parent.height / 2 - height / 2
            radius: 13
            color: switchConnect.checked ? "#17a81a" : "#ffffff"
            border.color: switchConnect.checked ? "#17a81a" : "#cccccc"

            Rectangle {
                x: switchConnect.checked ? parent.width - width : 0
                width: 26
                height: 26
                radius: 13
                color: switchConnect.down ? "#cccccc" : "#ffffff"
                border.color: switchConnect.checked ? (switchConnect.down ? "#17a81a" : "#21be2b") : "#999999"
            }
        }

        contentItem: Text {
            id: switchText
            text: switchConnect.text
            font: switchConnect.font
            opacity: enabled ? 1.0 : 0.3
            color: switchConnect.checked ? "#81848c" : "#21be2b"
            verticalAlignment: Text.AlignVCenter
            leftPadding: switchConnect.indicator.width + switchConnect.spacing
        }
    }

    Rectangle {
        id: rectangleRobot
        height: 120
        radius: 10
        color: "#17191e"
        anchors.left: rectangleTop.left
        anchors.right: rectangleTop.right
        anchors.top: rectangleTop.bottom
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 20

        Label {
            id: labelIP
            font.pointSize: 12
            color: "#81848c"
            text: qsTr("IP: Non connected")
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 30
            anchors.topMargin: 20
        }

        Label {
            id: labelPort
            font.pointSize: 12
            color: "#81848c"
            text: currPort
            anchors.left: parent.left
            anchors.top: labelIP.bottom
            anchors.leftMargin: 30
            anchors.topMargin: 30
        }
    }

    Rectangle {
        id: rectangleLoader
        height: 60
        radius: 10
        color: "#17191e"
        anchors.left: rectangleTop.left
        anchors.right: rectangleTop.right
        anchors.top: rectangleRobot.bottom
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 10

        Label {
            id: labelLoader
            font.pointSize: 12
            color: "#81848c"
            text: qsTr("Loader: Non connected")
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 30
            anchors.topMargin: 20
        }
    }

    Connections{
        target: backend

        function onIsVisible(isVisible){
            rectangleTop.visible = isVisible
            rectangle.visible = isVisible
        }

        function onSetIP(ip){
            labelIP.text = ip
        }

        function onSetPort(port){
            currPort = port
        }
    }

}
