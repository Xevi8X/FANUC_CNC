import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

Button {
    id: btnTopBar
    flat: true
    icon.color: "#ffffff"

    //Custom properties
    property url btnIconSource: "../images/svg_images/minimize_icon.svg"
    property color btnColorDefault: "#395bbf"
    property color btnColorMouseOver: "#23272E"
    property color btnColorClicked: "#00a1f1"


    QtObject{
        id: internal

        //Mouse over and click change
        property color dynamicColor: btnTopBar.down ? btnColorClicked : (btnTopBar.hovered ? btnColorMouseOver : btnColorDefault)
    }

    width: 35
    height: 35

    background: Rectangle{
           id: bgBtn
           color: internal.dynamicColor

           Image {
               id: iconBtn
               source: btnIconSource
               anchors.verticalCenter: parent.verticalCenter
               anchors.horizontalCenter: parent.horizontalCenter
               height: 16
               width: 16
               visible: false
               fillMode: Image.PreserveAspectFit
               antialiasing: false
           }

           ColorOverlay{
               anchors.fill: iconBtn
               source: iconBtn
               color: "#ffffff"
               antialiasing: false
           }
       }

}
