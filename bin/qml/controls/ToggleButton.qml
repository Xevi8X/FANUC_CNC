import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

Button {
    id: btnToggle
    flat: true

    //Custom properties
    property url btnIconSource: "../images/svg_images/menu_icon.svg"
    property color btnColorDefault: "#002b5b"
    property color btnColorMouseOver: "#23272E"
    property color btnColorClicked: "#00a1f1"


    QtObject{
        id: internal

        //Mouse over and click change
        property color dynamicColor: btnToggle.down ? btnColorClicked : (btnToggle.hovered ? btnColorMouseOver : btnColorDefault)
    }

    implicitWidth: 70
    implicitHeight: 60
    
    background: Rectangle {
        id: bgBtn
        color: internal.dynamicColor

        
        Image {
            id: iconBtn
            source: btnIconSource
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 25
            width: 25
            fillMode: Image.PreserveAspectFit
            visible: false
        }

        ColorOverlay{
            anchors.fill: iconBtn
            source: iconBtn
            color: "#ffffff"
            antialiasing: false
        }
    }
        
}
