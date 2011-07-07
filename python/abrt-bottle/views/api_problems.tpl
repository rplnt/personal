%include header.tpl title='API list problems'

<div class="main">
%for id, time, reason in api:
    <div class="problem">
        <span class="time">
            {{time}}
        </span>
        <span class="reason">
            {{reason}}
        </span>
        <a href="/problems/{{id}}">{{id}}</a>
    </div>
%end
</div>

%include footer.tpl