(function($){
    var $content_md = $('#div_id_content_md');
    var $content_ck = $('#div_id_content_ck');
    var $is_markdown = $('input[name=is_markdown]');
    var switch_editor = function(is_markdown) {
        if (is_markdown) {
            $content_md.show();
            $content_ck.hide();
        } else {
            $content_md.hide();
            $content_ck.show();
        }
    }
    $is_markdown.on('click', function() {
        switch_editor($(this).is(':checked'));
    });
    switch_editor($is_markdown.is(':checked'));
})(jQuery);
