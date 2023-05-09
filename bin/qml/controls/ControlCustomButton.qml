import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

Button{
    id: btnControl
    text: qsTr("Left Menu Text")

    // CUSTOM PROPERTIES
    property url btnIconSource: "../images/svg_images/one_up_icon.svg"
    property color btnColorDefault: "#282c34"
    property color btnColorHovered: "#23272E"
    property color btnColorClicked: "#00a1f1"
    property int iconWidth: 12
    property int iconHeight: 12
    property bool isActiveMenu: false

    QtObject{
        id: internal

        property color dynamicColor: btnControl.down ? btnColorClicked : (btnControl.hovered ? btnColorHovered : btnColorDefault)

    }

    implicitWidth: 50
    implicitHeight: 50

    background: Rectangle{
        id: bgBtn
        color: internal.dynamicColor
        radius: 8

    }

    contentItem: Item{
        anchors.fill: parent
        id: content
        Image {
            id: iconBtn
            source: btnIconSource
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            sourceSize.width: iconWidth
            sourceSize.height: iconHeight
            fillMode: Image.PreserveAspectFit
            visible: false
            antialiasing: true
        }

        ColorOverlay{
            anchors.fill: iconBtn
            source: iconBtn
            color: "#ffffff"
            anchors.verticalCenter: parent.verticalCenter
            antialiasing: true
            width: iconWidth
            height: iconHeight
        }
    }
}
