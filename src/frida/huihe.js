Java.perform(
    function () {

        var hookClass = Java.use('com.yuyh.library.nets.encryption.AesEncryptUtil')

         hookClass.encrypt.implementation = function() {
          var ret = this.encrypt.apply(this, arguments);

             console.log(arguments[0])
             console.log(arguments[1])
          return ret;
        }
    }
)

rpc.exports = {
    getme: function (random_str, public_key) {
        var res = "";
        Java.perform(
            function () {
                var hookClass = Java.use("com.yuyh.library.nets.encryption.RSAUtils");
                res = hookClass.encryptedDataOnJava(random_str, public_key);
            }
        )
        return res;
    },
     getmd: function (str1, str2) {
        var res = "";
        Java.perform(
            function () {
                var hookClass = Java.use("com.yuyh.library.nets.encryption.AesEncryptUtil");
                res1 = hookClass.encrypt(str1, str2);
            }
        )
        return res;
    }


};


