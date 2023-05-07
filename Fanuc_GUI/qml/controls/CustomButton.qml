import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

Button {
    id: button
    
    // Custom properties
    property color colorDefault: "#4891d9"
    property color colorMouseOver: "#55AAFF"
    property color colorPressed: "#3F7EBD"
    
    QtObject{
        id: internal
        
        property color dynamicColor: button.down ? colorPressed : (button.hovered ? colorMouseOver : colorDefault)
    }

    text: qsTr("Button")
    contentItem: Item{
        Text{
            id: name
            font: button.font
            color: "#282c34"
            text: button.text
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    background: Rectangle{
        color: internal.dynamicColor
        radius: 10
    }
    

}
