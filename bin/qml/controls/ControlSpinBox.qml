import QtQuick
import QtQuick.Controls

SpinBox {
    id: control
    value: 0
    from: -5
    to: 5
    editable: false

    contentItem: TextInput {
        z: 2
        text: control.textFromValue(control.value, control.locale)

        font: control.font
        color: "#81848c"
        horizontalAlignment: Qt.AlignHCenter
        verticalAlignment: Qt.AlignVCenter

        readOnly: !control.editable
        validator: control.validator
        inputMethodHints: Qt.ImhFormattedNumbersOnly
    }

    up.indicator: Rectangle {
        x: control.mirrored ? 0 : parent.width - width
        height: parent.height
        implicitWidth: 40
        implicitHeight: 40
        color: control.up.pressed ? "#00a1f1" : "#282c34"
        border.color: "#81848c"

        Text {
            text: "+"
            font.pixelSize: control.font.pixelSize * 2
            color: "#81848c"
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    down.indicator: Rectangle {
        x: control.mirrored ? parent.width - width : 0
        height: parent.height
        implicitWidth: 40
        implicitHeight: 40
        color: control.down.pressed ? "#00a1f1" : "#282c34"
        border.color: "#81848c"

        Text {
            text: "-"
            font.pixelSize: control.font.pixelSize * 2
            color: "#81848c"
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    background: Rectangle {
        implicitWidth: 140
        color: "#282c34"
        border.color: "#81848c"
    }
}
