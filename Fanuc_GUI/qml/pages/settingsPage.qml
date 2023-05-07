import QtQuick 2.15
import QtQuick.Controls 6.3

Item {

    Rectangle {
        id: rectangle
        color: "#1a5f7a"
        anchors.fill: parent

        Label {
            id: label
            color: "#ffffff"
            text: qsTr("Settings Page")
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 16
        }
    }

}
