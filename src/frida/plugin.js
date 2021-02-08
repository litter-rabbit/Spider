Java.perform(function () {
    Java.enumerateClassLoaders({
        "onMatch": function(loader) {
            if (loader.toString().startsWith("com.tencent.shadow.core.loader.classloaders.PluginClassLoader")) {
                Java.classFactory.loader = loader;
            }
        },
        "onComplete": function() {
            console.log("success");
        }
    });

    var videoController = Java.classFactory.use("com.iqiyi.plugin.widget.dkplayer.controller.VideoController");
    videoController.setVip.implementation = function() {
        console.log("hook setVip");
        this.setVip(true);
    };

    var pluginEnum = Java.classFactory.use("com.iqiyi.plugin.base.PluginEnum");
    var String = Java.use("java.lang.String");
    pluginEnum.getValue.implementation = function() {
        var value = this.getValue();
        if (this == "VIP") {
            var vip = String.$new("1");
            this.setValue(vip);
            return vip;
        } else {
            return value;
        }
    }

});