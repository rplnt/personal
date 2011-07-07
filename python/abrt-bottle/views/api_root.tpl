%include header.tpl title='API Entry Point'

<div class="main">
%for id in api.keys():
<ul>
<li><a href="{{id}}">{{api[id]}}</a></li>
<ul>
%end
</div>

%include footer.tpl