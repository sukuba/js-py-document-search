// full text search using JsNgram
// https://github.com/sukuba/js-py-document-search

$(document).ready(function(){
  
  var $q = $('#q');
  var ignore = /[\s,.，．、。]/g;
  
  JsNgram.errorSelector = $('#error');
  JsNgram.resultSelector = $('#result');
  JsNgram.size = 2;
  JsNgram.indexBase = 'idx/';
  JsNgram.textBase = 'txt/';
  JsNgram.keySeparator = '/';
  JsNgram.verbose = 1;
  
  var dbBase = 'db/';
  var fileinfo = 'fileinfo.json';
  var ignoreMessage = ' / 空白やピリオドなどの区切り記号は検索対象外なので消しました。';
  var ignoreDelay = 2400; // milliseconds
  
  // 日本語メッセージ
  JsNgram.msgOnSearch = '探しています ... お待ちください。';
  JsNgram.ignoreBlank = '探したい言葉を入れてください。'; // shown at console
  JsNgram.resultNone = '見つかりませんでした。';
  JsNgram.resultCount = '%%か所が %%件の文書に見つかりました。';
  JsNgram.askToShowFound = '部分一致も見ますか？';
  JsNgram.askToShowNextDocs = '続きを見る ... %%件目より後の文書';
  JsNgram.askToShowNextHits = '+ 続きを見る ... %%か所目より後の一致';
  JsNgram.partialMatches = '(部分一致)';
  
  // 使い方のヒント
  JsNgram.resultSelector.append(
    [
      '<ul><li>',
      [
        '任意のキーワードを含む文書を検索します。',
        '英数字は半角で。',
        'カタカナは全角で。',
        'スペースを使っての複合検索はできません。'
      ].join('</li><li>'),
      '</li></ul>'
    ].join('')
  );
  
  // fileinfo を取り込む。
  $.ajax(fileinfo, JsNgram.ajaxJson).done(function(result){
    JsNgram.titleInfo = result;
  }).fail(function(xhr, ajaxOptions, thrownError){
    var msg =xhr.status + ' / ' + thrownError;
    var msg2 = this.url + ' / ' + msg;
    console.log(msg2);
  });
  
  // fileinfo 形式を、タイトル行に使う。配列先頭がタイトル。
  JsNgram.loadTitleInfo = function(selector, docId) {
    var titleFn = this.makeResultHtml.title;
    var url = this.convertIdToUrl(docId);
    var info = this.titleInfo[docId];
    var title = docId;
    var data = [];
    if(info && Array.isArray(info) && info[0]) {
      title = info[0];
      data = info.slice(1);
    }
    title = this.escapeHtml(title);
    
    return(selector.append(titleFn(url, title, data)));
  };
  
  // リンク先を .txt でなく、db/ の元文書に飛ばす
  JsNgram.convertIdToUrl = function(docId) {
    var withoutDotTXT = docId.substr(0, docId.length - 4);
    return(encodeURI(dbBase + withoutDotTXT));
  };
  
  // 検索機能
  function enterSearch() {
    var what = $q.val();
    if(ignore.test(what)) {
      setTimeout(
        function(){
          JsNgram.appendErrorMessage(ignoreMessage);
        }, 
        ignoreDelay
      );
      what = what.replace(ignore, '');
      $q.val(what);
    }
    JsNgram.search(what);
  }
  
  $('#search').click(function(){
    enterSearch();
  });
  
  $q.keypress(function(k){
    if(k.which == 13) {
      enterSearch();
      return(false);
    }
  });
  
  $q.focus();
});
