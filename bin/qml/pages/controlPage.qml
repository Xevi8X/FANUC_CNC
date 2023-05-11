import QtQuick
import QtQuick.Controls
import "../controls"
import QtQuick.Layouts 6.3

Item {
    property string currPort: "Port: Non connected"

    Connections{
        target: backend

        function onIsVisible(isVisible){
            rectangleTop.visible = isVisible
            rectangleProgControlBtns.visible = isVisible
        }

        function onSetIP(ip){
            labelIP.text = ip
        }

        function onSetPort(port){
            currPort = port
        }

        function onSetSpeed(value){
            speed = value
        }

        function onSetZ(value){
            z_offset = value
        }

        function onPrintTime(time){
            logsTextArea.append(time)
        }

        function onLineNo(no){
            labelActualLine.text = no
        }
    }

    Rectangle {
        id: rectangleProgControlBtns
        width: 200
        height: 130
        color: "#17191e"
        radius: 8
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 50
        anchors.topMargin: 50

        Row {
            id: btnsRectangle
            width: 170
            height: 60
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.left: labelControlsBtns.left
            anchors.top: labelActualLine.bottom

            anchors.leftMargin: 5
            anchors.topMargin: 15
            spacing: 10

            ControlCustomButton {
                id: upOne
                anchors.leftMargin: 5
                anchors.topMargin: 5
                anchors.rightMargin: 10
                onClicked:{
                    backend.oneStep()
                }
            }
            ControlCustomButton {
                id: playBtn
                anchors.topMargin: 5
                btnIconSource:  "../images/svg_images/play_icon.svg"
                onClicked:{
                    backend.start()
                }
            }
            ControlCustomButton {
                id: pauseBtn
                anchors.topMargin: 5
                anchors.leftMargin: 10
                btnIconSource:  "../images/svg_images/pause_icon.svg"
                onClicked:{
                    backend.pause()
                }
            }
        }

        Label {
            id: labelControlsBtns
            font.pointSize: 12
            color: "#81848c"
            text: qsTr("Control buttons")
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 10
            anchors.topMargin: 10
        }

        Label {
            id: labelActualLine
            color: "#81848c"
            text: qsTr("Actual Line #:")
            anchors.left: labelControlsBtns.left
            anchors.top: labelControlsBtns.bottom
            anchors.topMargin: 5
            anchors.leftMargin: 0
            font.pointSize: 10
        }
    }

    Rectangle {
        id: rectangleHWControls
        width: 200
        height: 170
        color: "#17191e"
        radius: 8
        anchors.left: rectangleProgControlBtns.left
        anchors.top: rectangleProgControlBtns.bottom
        anchors.leftMargin: 0
        anchors.topMargin: 10

        Label {
            id: labelZControl
            color: "#81848c"
            text: qsTr("Dynamic Z control")
            anchors.left: parent.left
            anchors.top: parent.top
            font.pointSize: 12
            anchors.leftMargin: 10
            anchors.topMargin: 10
        }

        Label {
            id: labelSpindleControl
            color: "#81848c"
            text: qsTr("Spindle speed control")
            anchors.left: parent.left
            anchors.top: labelZControl.bottom
            anchors.topMargin: 70
            anchors.leftMargin: 10
            font.pointSize: 12
        }

        ControlSpinBox{
            id: spinbox_z
            anchors.top: labelZControl.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 10
            onValueModified: {
                    backend.setZ(spinbox_z.value)
                }

        }

        CustomSlider{
            id: speedSlider
            anchors.top: labelSpindleControl.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 5
            from: 0
            value: 25
            to: 100
            onMoved: {
                backend.setSpeed(speedSlider.value)
            }
        }
    }

    TextArea {
        id: logsTextArea
        anchors.left: rectangleProgControlBtns.right
        anchors.right: parent.right
        anchors.top: rectangleProgControlBtns.top
        anchors.bottom: rectangleHWControls.bottom
        wrapMode: Text.WordWrap
        readOnly: true
        clip: true
        anchors.rightMargin: 20
        anchors.leftMargin: 20
        anchors.bottomMargin: 0
        anchors.topMargin: 0
        placeholderText: qsTr("Logs")
        color: "#ffffff"

        background: Rectangle{
            color: "#17191e"
            radius: 10
        }
    }

}
