code4fun.laserOn()

basic.forever(function () {
    if (code4fun.laserBeamBlocked()) {
        basic.showIcon(IconNames.No)
    } else {
        basic.showIcon(IconNames.Yes)
    }
})
