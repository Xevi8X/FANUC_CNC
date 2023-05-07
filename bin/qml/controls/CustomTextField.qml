import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

TextField {
    id: textField

    // Custom properties
    property color colorDefault: "#282c34"
    property color colorMouseOver: "#242831"
    property color colorOnFocus: "#2B2F38"

    QtObject{
        id: internal

        property color dynamicColor: textField.focus ? colorOnFocus : (textField.hovered ? colorMouseOver : colorDefault)
    }

    implicitWidth: 300
    implicitHeight: 40
    placeholderText: qsTr("Type something")
    color: "#ffffff"
    background: Rectangle{
        color: internal.dynamicColor
        radius: 10
    }

    selectByMouse: true
    selectedTextColor: "#FFFFFF"
    selectionColor: "#ff007f"
    placeholderTextColor: "#81848c"


}
