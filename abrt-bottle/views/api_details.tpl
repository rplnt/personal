%include header.tpl title='Details of problem'+pid
        
<div class="main">
    <span class="title">Details of {{pid}}</span>
    %for key,value in api.items():
        <div class="item">
            <span class="name">{{key}}</span>
            <span class="text">{{value}}</span>
        </div>
    %end
</div>

%include footer.tpl