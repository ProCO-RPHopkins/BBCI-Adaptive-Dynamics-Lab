import {simulate,metrics} from './engine.js';
self.onmessage=e=>{try{const {person,arm,options}=e.data;const selected=simulate(person,arm,options),sham=simulate(person,'sham',options);self.postMessage({selected,sham,metrics:metrics(selected,person.calibration),shamMetrics:metrics(sham,person.calibration)});}catch(err){self.postMessage({error:err.message})}};
