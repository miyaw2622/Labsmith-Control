classdef MyClass < handle
    events
        MyEvent
    end
    
    methods
        function triggerEvent(obj)
            notify(obj, 'MyEvent');
        end
    end
end

% Listener Example
obj = MyClass();
addlistener(obj, 'MyEvent', @(src, event) disp('Event triggered!'));
obj.triggerEvent();