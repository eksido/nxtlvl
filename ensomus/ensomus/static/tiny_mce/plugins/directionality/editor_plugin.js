(function () {
    tinymce.create("tinymce.plugins.Directionality", {
        init: function (b, c) {
            var d = this;
            d.editor = b;
            function a(e) {
                var h = b.dom, g, f = b.selection.getSelectedBlocks();
                if (f.length) {
                    g = h.getAttrib(f[0], "dir");
                    tinymce.each(f, function (i) {
                        if (!h.getParent(i.parentNode, "*[dir='" + e + "']", h.getRoot())) {
                            if (g != e) {
                                h.setAttrib(i, "dir", e)
                            } else {
                                h.setAttrib(i, "dir", null)
                            }
                        }
                    });
                    b.nodeChanged()
                }
            }

            b.addCommand("mceDirectionLTR", function () {
                a("ltr")
            });
            b.addCommand("mceDirectionRTL", function () {
                a("rtl")
            });
            b.addButton("ltr", {title: "directionality.ltr_desc", cmd: "mceDirectionLTR"});
            b.addButton("rtl", {title: "directionality.rtl_desc", cmd: "mceDirectionRTL"});
            b.onNodeChange.add(d._nodeChange, d)
        }, getInfo: function () {
            return {
                longname: "Directionality",
                author: "Moxiecode Systems AB",
                authorurl: "http://tinymce.moxiecode.com",
                infourl: "http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/directionality",
                version: tinymce.majorVersion + "." + tinymce.minorVersion
            }
        }, _nodeChange: function (b, a, e) {
            var d = b.dom, c;
            e = d.getParent(e, d.isBlock);
            if (!e) {
                a.setDisabled("ltr", 1);
                a.setDisabled("rtl", 1);
                return
            }
            c = d.getAttrib(e, "dir");
            a.setActive("ltr", c == "ltr");
            a.setDisabled("ltr", 0);
            a.setActive("rtl", c == "rtl");
            a.setDisabled("rtl", 0)
        }
    });
    tinymce.PluginManager.add("directionality", tinymce.plugins.Directionality)
})();