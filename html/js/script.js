$(document).ready(function () {
    //use this path to data if no hash is set
    var url_hash = "demo.dpa-newslab.com/newsstream/branchendienst/news/v3/";


    //debugging
    //DELETE Storage on reload
    /*
    $.each(localStorage, function (index, value) {
        localStorage.removeItem(index);
    });
    */

    //////VARS//////////////////////////////////////

    var id_array = [];
    var news_data = "";
    var deeplink_day = false;
    var deeplink_day_url = "";
    var temp_file_name = "";
    var rootlabel = "";
    var category = "";
    var placeholder = "";
    var email_address = "";
    var email_subject = "";

    //////HASH///////////////
    var url = document.location.href;
    var temp_pos = url.lastIndexOf("#");
    //there is a hash
    if (temp_pos !== -1) {
        var temp_str = url.substr(temp_pos + 1);
        if (temp_str.indexOf("json") !== -1) {
            if (temp_str.indexOf("index") !== -1) {
                //e.g. http://cornelia-geissler.de/temp_1/dpa/dpa-Branchendienst/#demo.dpa-newslab.com/newsstream/branchendienst/news/v2/20161012-index.json
                //console.log("deeplink:day");
                temp_file_name = temp_str.substring(temp_str.lastIndexOf("/") + 1);
                url_hash = temp_str.substring(0, temp_str.lastIndexOf("/") + 1);
                built_content(temp_file_name);
                deeplink_day = true;
                deeplink_day_url = temp_file_name;
            } else {
                //e.g. http://cornelia-geissler.de/temp_1/dpa/dpa-Branchendienst/#demo.dpa-newslab.com/newsstream/branchendienst/news/v2/20161012/1af33851798ba58f303e74b5b97f661a.json
                //console.log("deeplink:detail");
                var url_hash_1 = temp_str.substring(0, temp_str.lastIndexOf("/"));
                url_hash = url_hash_1.substring(0, url_hash_1.lastIndexOf("/") + 1);
                temp_file_name = url_hash;
                var temp_file_detail = url_hash_1.substring(url_hash_1.lastIndexOf("/") + 1);
                var temp_file_date = temp_file_detail + "-index.json";
                $.getJSON("http://" + temp_str, function (data) {
                    built_content(temp_file_date, data.section, data.id, data.text);
                });
                deeplink_day = true;
                deeplink_day_url = temp_file_date;
            }
        } else {
            //e.g. "http://cornelia-geissler.de/temp_1/dpa/dpa-Branchendienst/"
            //console.log("deeplink:start");
            url_hash = temp_str;
        }
    }

    $.getJSON("//" + url_hash + "index.json?123", function (data) {
        rootlabel = data.title;
        var first_element = true;
        $(".modal-body").html(data.description);
        $(".start").html(rootlabel);
        $("#appTitle").html(rootlabel);
        placeholder = data.placeholder;
        email_address = data.email;
        email_subject = data.subject;

        $.each(data.chapters, function (index, value) {
            if (first_element === true && deeplink_day === false) {
                built_content(value);
                first_element = false;
                //info modal content
                $("#dpa_main").html("<h3 class='start'>" + rootlabel + "<br>" + index + "</h3>");
            }
            if (value !== deeplink_day_url) {
                $('.navbar-select').append("<option value='" + value + "'>" + index + "</option>");
            } else {
                $('.navbar-select').append("<option selected value='" + value + "'>" + index + "</option>");
            }
        });
        $("#info-modal").modal('show');
    });

    $('.navbar-select').change(function (e) {
        $("#dpa_main").unbind("click");
        $(".dropdown-menu,.nav-pills").unbind("click");
        $(".logo_small, .logo_small_big").unbind("click");
        var temp_date = $(".navbar-select option[value='" + $(this).val() + "']").html();

        $("#dpa_main").html("<h3 class='start'>" + rootlabel + "<br>" + temp_date + "</h3>");
        built_content($(this).val());
        $("#selected").html("");
        $("#selectedBig").html("");
        $(".nav-pills li").removeClass("active");
        //set url hash
        parent.location.hash = url_hash + $(this).val();
    });

    $('.info').click(function (e) {
        $("#info-modal").modal('show');
    });

    function built_content(date_data, page_content, detail_id, detail_text) {
        $("#nav_all ul li").remove();
        $(".dropdown-menu li").remove();

        $.getJSON("//" + url_hash + date_data, function (data) {
            var nav_wide = "";
            var i = 0;
            var deeplink_caption = "";
            var deeplink_highlight = "";
            var sort_data = [];

            news_data = data;
            $.each(data.news, function (index, value) {
                if (page_content !== undefined) {
                    if (page_content === index) {
                        deeplink_caption = value.label;
                        deeplink_highlight = " class='active'";
                    }
                }
                value.index = index;
                sort_data.push(value);
                i++;

                nav_wide = nav_wide + "<li" + deeplink_highlight + "><a id='" + index + "' class='" + i + "'>" + value.label + "</a></li>";
                deeplink_highlight = "";
            });

            built_mobile_menue(data, sort_data);
            $("#nav_all ul").append(nav_wide);
            $("#nav_all ul").fadeIn("slow");

            //deeplink
            if (page_content !== undefined) {
                var article_text = detail_text;
                var article_id = detail_id;
                built_page_content(page_content, article_id, article_text);

                $("#selected").html(deeplink_caption);
                $("#selectedBig").html("&nbsp;&bull; " + deeplink_caption);
            }
        });

        $(".navbar-toggle").click(function (e) {
            if ($('.nav').css("display") === "none") {
                $('.nav').slideDown("slow", function () {
                    $(".navbar-toggle").trigger("click");
                });
            }
        });

        $(".dropdown-menu,.nav-pills").click(function (e) {
            $('#navbar .nav').css("display", "none");
            id_array.length = 0;
            $(".nav-pills li").removeClass("active");
            $(this).children("li:eq( " + (e.target.className - 1) + " )").addClass("active");
            $("#selected").html(e.target.text);
            $("#selectedBig").html("&nbsp;&bull; " + e.target.text);
            built_page_content(e.target.id);
            parent.location.hash = url_hash + news_data.news[e.target.id].docs[0].document;
        });

        var temp = "";
        $("#dpa_main").click(function (e) {
            if (e.target.className === "dpa_teaser" || e.target.className === "panel-title" || e.target.className === "panel-date") {
                var temp_id = $("#" + e.target.parentNode.id).find("a").get(1).id;
                $("#collapse" + e.target.parentNode.id).collapse('toggle');
                $.getJSON("//" + url_hash + temp_id, function (data) {
                    $("#collapse" + e.target.parentNode.id + " div").text(data.text);
                    parent.location.hash = url_hash + temp_id;
                });
            }
            if (e.target.className === "panel-heading accordion-toggle") {
                var temp_id = $("#" + e.target.id).find("a").get(1).id;
                $("#collapse" + e.target.id).collapse('toggle');
                $.getJSON("//" + url_hash + temp_id, function (data) {
                    $("#collapse" + e.target.id + " div").text(data.text);
                    parent.location.hash = url_hash + temp_id;
                });
            }
            //click detail
            if (e.target.hash !== undefined) {
                $.getJSON("//" + url_hash + e.target.id, function (data) {
                    console.log(e.target.hash)
                    $(e.target.hash + " div").text(data.text);
                    parent.location.hash = url_hash + e.target.id;
                });
            }
            //click selectbox
            if (e.target.className === "selectbox" || e.target.className === "selectbox active") {
                if (e.target.className === "selectbox active") {
                    localStorage.removeItem(e.target.id);
                    var temp = e.target.attributes.name.value;
                    $("input.note:eq(" + e.target.attributes.name.value + ")").attr("disabled", true);
                    $("input.note:eq(" + e.target.attributes.name.value + ")").val("");
                } else {
                    temp = new Date().toLocaleDateString() + "," + category + "," + e.target.id.slice(4) + ",true";
                    localStorage[e.target.id] = temp;
                    $("input.note:eq(" + e.target.attributes.name.value + ")").attr("disabled", false);
                }
                $("#" + e.target.id).toggleClass("active");
            }

            if (e.target.className === "note") {
                $("input.note:eq(" + e.target.name + ")").change(function () {
                    var temp = $(this).val();
                    if (temp === "") {
                        temp = "true";
                    }
                    temp = new Date().toLocaleDateString() + "," + category + "," + $(this).next().attr("id").slice(4) + "," + temp;
                    localStorage[$(this).next().attr("id")] = temp;
                });
            }
            //fade in send button
            if (localStorage.length > 0) {
                $("#email_btn").fadeIn("slow");
            } else {
                $("#email_btn").fadeOut("slow");
            }
        });
        
        $("#appTitle").click(function (e) {
            var temp_pos = url.lastIndexOf("#");
            if (temp_pos !== -1) {
                var temp_str = url.substr(0, temp_pos + 1);
                window.open(temp_str + url_hash, '_self');
            } else {
                window.open(url, '_self');
            }
        });
    }

    function built_page_content(page_id, article_id, article_text) {
        var content = "";
        var top_position = 0;
        category = page_id;

        $.each(news_data.news[page_id].docs, function (index, value) {
            id_array[value.id] = value.sectors;
            var add_active_UP = "";
            var add_active_DOWN = "";
            var disabled = "disabled";
            var input_content = "";

            $.each(localStorage, function (index1, value1) {
                if (index1.indexOf(value.id) !== -1) {
                    if (index1.indexOf("UP") !== -1) {
                        add_active_UP = " active";
                        disabled = "";
                    }
                    if (index1.indexOf("DOWN") !== -1) {
                        add_active_DOWN = " active";
                        disabled = "";
                        if (value1.substring(value1.lastIndexOf(",") + 1) !== "true") {
                            input_content = value1.substring(value1.lastIndexOf(",") + 1);
                        }
                    }
                }
            });

            var temp_1 = value.createdAt.split("T");
            if (article_id !== value.id) {
                var article = "";
                var temp = " collapse";
            } else {
                article = article_text;
                top_position = index;
            }
            content = content + "<div class='panel panel-default'><div class='panel-heading accordion-toggle' id='" + index + "'><span class='panel-date'>" + format_date(temp_1[0]) + ", <a href='" + value.sourcelink + "' target='_blank'>" + value.source + "</a></span><h3 class='panel-title'><a data-toggle='collapse' id ='" + value.document + "' data-parent='#accordion' href='#collapse" + index +
                    "'>" + value.title + "</a><input class='note' type='text' value='" + input_content + "' name='" + index + "' placeholder='" + placeholder + "' " + disabled + "><span class='selectbox" + add_active_DOWN + "' id ='DOWN" + value.id + "' name='" + index + "'></span> </h3>" +
                    "<span class='dpa_teaser'>" + value.subtitle + "</span>  </div>" +
                    "<div id='collapse" + index + "' class='panel-collapse" + temp + "'><div class='panel-body'>" + article + "</div></div></div>";
            temp = "";
        });
        $("#dpa_main").html(content);
        if (top_position === 0) {
            $('html,body').animate({scrollTop: $(".panel:eq(" + top_position + ")").offset().top - 72}, 0);
        } else {
            $('html,body').animate({scrollTop: $(".panel:eq(" + top_position + ")").offset().top - 56}, 0);
        }
    }

    function built_mobile_menue(data, sort_data) {
        sort_data.sortByProp('label');
        var nav_1 = "", nav_2 = "", nav_3 = "", nav_4 = "", nav_5 = "";
        var unicode = "";
        $.each(sort_data, function (index, value) {
            unicode = value.label.charCodeAt(0);
            if (unicode <= 67) {
                nav_1 = nav_1 + "<li><a id='" + value.index + "'>" + value.label + "</a></li>";
            }
            if (unicode >= 68 && unicode <= 71) {
                nav_2 = nav_2 + "<li><a id='" + value.index + "'>" + value.label + "</a></li>";
            }
            if (unicode >= 72 && unicode <= 76) {
                nav_3 = nav_3 + "<li><a id='" + value.index + "'>" + value.label + "</a></li>";
            }
            if (unicode >= 77 && unicode <= 82) {
                nav_4 = nav_4 + "<li><a id='" + value.index + "'>" + value.label + "</a></li>";
            }
            if (unicode >= 83 && unicode <= 500) {
                nav_5 = nav_5 + "<li><a id='" + value.index + "'>" + value.label + "</a></li>";
            }
        });
        $(".dropdown-menu:eq( 0 )").append(nav_1);
        $(".dropdown-menu:eq( 1 )").append(nav_2);
        $(".dropdown-menu:eq( 2 )").append(nav_3);
        $(".dropdown-menu:eq( 3 )").append(nav_4);
        $(".dropdown-menu:eq( 4 )").append(nav_5);
    }

    $("#email_btn a").click(function (e) {
        var temp_all = "";
        $.each(localStorage, function (index, value) {
            if (value.length > 10) {
                temp_all = temp_all + encodeURIComponent(value) + "%0D%0A";
            }
        });
        $("#email_btn a").attr("href", "mailto:" + email_address + "?subject=" + email_subject + "&body=" + temp_all);
    });

    //HELPER/////////////
    function format_date(date_stamp) {
        var temp = date_stamp.split("-");
        var date = temp[2] + "." + temp[1] + "." + temp[0];
        return date;
    }
    Array.prototype.sortByProp = function (p) {
        return this.sort(function (a, b) {
            return (a[p] > b[p]) ? 1 : (a[p] < b[p]) ? -1 : 0;
        });
    };
});

