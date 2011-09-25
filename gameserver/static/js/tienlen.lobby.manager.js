/*jslint white: true, onevar: true, undef: true, newcap: true, nomen: true, regexp: true, plusplus: true, bitwise: true, strict: true, browser: true */
/*global $: true*/

"use strict";
var TL = TL || {};

TL.manager = {
    createTable: function (tableName) {
        $.ajax({
            type: "POST",
            url: "/tienlen/tables/create",
            data: {
                name: tableName
            },
            success: function (data) {
                alert(data);
            }
        });
    },

    signIn: function (username, password, callback) {
        $.ajax({
            type: "POST",
            url: "/accounts/login",
            data: {
                email: username,
                password: password
            },
            success: function (data) {
                callback(JSON.parse(data));
            }
        });
    },

    createAccount: function (username, password, callback) {
        $.ajax({
            type: "POST",
            url: "/accounts/create",
            data: {
                email: username,
                password: password
            },
            success: function (data) {
                callback(JSON.parse(data));
            }
        });
    }
};

