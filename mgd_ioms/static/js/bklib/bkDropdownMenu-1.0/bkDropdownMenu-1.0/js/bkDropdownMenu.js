 /*!
  * bkDropdownMenu v1.0
  * author ：蓝鲸智云
  * Copyright (c) 2012-2017 Tencent BlueKing. All Rights Reserved.
  */
(function(factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['jquery'], factory);
    } else if (typeof exports === 'object') {
        // Node/CommonJS
        module.exports = factory(require('jquery'));
    } else {
        // Browser globals
        factory(window.jQuery);
    }
}(function($) {
    $.fn.bkDropdown = function(options) {
        var _this = this;
        var defaultOptions = {
            width: 0,
            trigger: 'mouseover', //触发方式 mouseover/click
            align: 'left', // 对齐方式 left/right
            onInit: null,
            onShow: null,
            onHide: null
        };

        var settings = $.extend({}, defaultOptions, options);

        function _guid() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
                return v.toString(16);
            });
        }

        function _show(target) {
            var OFFSET = 3; // 下拉框和触发器之间的空隙
            var triggerBtn = target.find('.bk-dropdown-trigger');
            var menuList = target.find('.bk-dropdown-content');
            var triggerBtnHeight = triggerBtn.outerHeight();
            var menuHeight = menuList.outerHeight();
            var docHeight = $(window).height();
            var triggerBtnOffset = triggerBtn.offset();
            var menuOffsetTop = triggerBtnHeight + OFFSET;
            var scrollTop = document.body.scrollTop;
            if ((docHeight - (triggerBtnOffset.top + triggerBtnHeight)) > (menuHeight + OFFSET)){
                menuList.removeAttr('style').css('top', menuOffsetTop + 'px')
            } else {
                menuList.removeAttr('style').css('bottom', menuOffsetTop + 'px')
            }
            menuList.addClass('is-show');
            settings.onShow && settings.onShow(target);
        }

        function _hide(target) {
            var triggerBtn = target.find('.bk-dropdown-trigger');
            var menuList = target.find('.bk-dropdown-content');
            menuList.removeClass('is-show'); 
            settings.onHide && settings.onHide(target);
        }

        function init(target) {
            var timer = 0;
            var triggerBtn = target.find('.bk-dropdown-trigger');
            var menuList = target.find('.bk-dropdown-content');

            // 宽度
            if (parseInt(settings.width)) {
                menuList.css('width', parseInt(settings.width) + 'px');
            }
            // 左右对齐方式
            if (settings.align == 'right') {
                menuList.addClass('right-align');
            } else if (settings.align == 'center') {
                menuList.addClass('center-align');
            } else {
                menuList.addClass('left-align');
            }

            // 绑定事件
            target.on('mouseover', function() {
                _show(target)
                clearTimeout(timer);
            });
            target.on('mouseout', function(event) {
                timer = setTimeout(function() {
                    _hide(target);
                }, 200)
            });
            
            // 注册对象
            target.data('bkDropdown', {
                uuid: _guid(),
                show: function() {
                    _show(target);
                },
                hide: function() {
                    _hide(target);
                }
            });

            settings.onInit && settings.onInit(target);
        }

        $.each(this, function(target) {
            var target = $(this);

            if (target && !target.data('bkDropdown')) {
                init(target);    
            }
        })
    }
}));