import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const root=process.cwd();
const runtime='C:/Users/홍종규/.cache/codex-runtimes/codex-primary-runtime/dependencies';
process.env.RUNTIME_NODE_MODULES=runtime+'/node/node_modules';
const {Presentation,PresentationFile}=await import(pathToFileURL(runtime+'/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs'));
const p=Presentation.create({slideSize:{width:1600,height:900}});
const build=path.join(root,'20_Projects/SGIS_MTV/.pptx-build');await fs.mkdir(build,{recursive:true});
const html=await fs.readFile(path.join(root,'20_Projects/SGIS_MTV/국데처MTV_작업계획서_V4_빈티지.html'),'utf8');
const C={bg:'#FFFAF0',ink:'#352E28',muted:'#75685B',line:'#C9BAA4',brown:'#89613E',head:'#E9DCC5',late:'#FBE3BD',red:'#953E24'};
const clean=s=>s.replace(/<br\s*\/?\s*>/g,'\n').replace(/<[^>]*>/g,'').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').trim();
function shape(s,g,x,y,w,h,fill,stroke='none',sw=0){return s.shapes.add({geometry:g,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:sw,style:'solid'}})}
function text(s,t,x,y,w,h,size=25,bold=false,color=C.ink,align='left'){const a=shape(s,'textbox',x,y,w,h,'none');a.text=t;a.text.style={typeface:'Malgun Gothic',fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',wrap:true,insets:0};return a;}
function slide(title,sub=''){const s=p.slides.add();s.background.fill=C.bg;text(s,title,64,42,1470,66,42,true);if(sub)text(s,sub,66,117,1468,48,21,false,C.muted);text(s,'국가데이터처 SGIS  /  MTV 작업계획 V4',64,850,1300,28,16,false,C.muted);text(s,String(p.slides.items.length).padStart(2,'0'),1460,850,75,28,16,false,C.muted,'right');s.speakerNotes.text='출처: 국데처MTV_작업계획서_V4_빈티지.html. 2026-10-12 기준 검토본입니다.';return s;}
const tableOwners=[];
function nativeTable(s,rows,widths,y=195,height=570,size=24){const t=s.tables.add({rows:rows.length,columns:rows[0].length,left:64,top:y,width:1472,height,columnWidths:widths,values:rows});t.borders.assign({fill:C.line,width:1,style:'solid'});for(let r=0;r<rows.length;r++){t.rows[r].height=r===0?58:(height-58)/(rows.length-1);for(let c=0;c<rows[0].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?C.head:(rows[r].includes('Worker2')?C.late:r%2?C.bg:'#F7F0E4');cell.text.style={typeface:'Malgun Gothic',fontSize:size,bold:r===0,color:C.ink,verticalAlignment:'middle',insets:12};}}tableOwners.push(p.slides.items.length);return t;}
// Cover
{const s=slide('SGIS 오픈플랫폼');text(s,'인프라 전환 및\nMTV 작업계획서',80,255,1440,220,67,true);text(s,'V4  빈티지 보고서',83,515,1000,55,30,false,C.brown);text(s,'2026. 10. 12.\n공무원·사업자 검토용 초안',83,640,1250,90,25,false,C.muted);}
{const s=slide('사업 범위 및 운영 현황');nativeTable(s,[['구분','현재 구성 / 계획'],['외부망','VMware HV 2대 / VM 13식'],['내부망','VMware HV 3대 / VM 26식'],['전환 방식','Worker1을 먼저 구축하고, MTV 이후 HV#01을 Worker2로 전환합니다.'],['스토리지','동일 EMC를 사용합니다. 원본 VMFS와 CSI 대상 볼륨을 함께 확보합니다.'],['범위','DB 레거시 풀은 재구성 대상에서 제외합니다.']],[290,1182],180,585,25);}
function attrs(s){return Object.fromEntries([...s.matchAll(/([\w-]+)="([^"]*)"/g)].map(m=>[m[1],m[2]]));}
const svgs=[...html.matchAll(/<svg\b[\s\S]*?<\/svg>/g)].map(m=>m[0]);
for(const [idx,svg]of svgs.entries()){
 const title=['외부망 AS-IS / TO-BE','내부망 AS-IS / TO-BE','동일 EMC 스토리지 이관 구성'][idx];
 const s=slide(title,idx<2?'Worker1은 선구축하며, 강조한 Worker2는 MTV 이후 재구성합니다.':'VMFS 원본 유지분과 CSI 대상 볼륨을 동시에 확보합니다.');
 const sc=1.16,ox=80,oy=166;
 // Native editable evidence from the supplied SVG, not a screenshot.
 for(const m of svg.matchAll(/<(rect|text|path)\b([^>]*?)(?:\/>|>([\s\S]*?)<\/text>)/g)){
  const a=attrs(m[2]),cl=a.class||'',k=m[1];
  if(k==='rect'){
   let fill='#FFFAF0',stroke=C.line,sw=1;
   if(cl.includes('server')){fill='#FFFDF6';stroke='#9D8B74'}if(cl.includes('pool')){fill='#EEE7D9';stroke='#B19A77'}if(cl==='vm'){fill='#E8DFCC';stroke='#A38B66'}
   if(cl.includes('late-server')){fill=C.late;stroke='#A14827';sw=3}if(cl.includes('late-badge')){fill=C.red;stroke='none'}
   if(cl.includes('panel-asis'))stroke='#656566';if(cl.includes('panel-tobe'))stroke=C.brown;
   shape(s,'rect',ox+(+a.x)*sc,oy+(+a.y)*sc,(+a.width)*sc,(+a.height)*sc,fill,stroke,sw);
  }else if(k==='text'){
   const t=clean(m[3]||'').replace('점선: ', '');let size=cl.includes('small')?16:cl.includes('stitle')?24:cl.includes('bold')?23:19;
   let color=cl.includes('phase-title')?'#FFFAF0':cl.includes('late-label')?'#FFFAF0':C.ink;
   const centered=a['text-anchor']==='middle',w=centered?(idx===2?((+a.x)===620?1250:550):190):Math.min(780,(1240-(+a.x))*sc);
   text(s,t,ox+(+a.x)*sc-(centered?w/2:0),oy+(+a.y)*sc-size*1.0,w,size*1.45,size,cl.includes('bold')||cl.includes('stitle')||cl.includes('late-label'),color,centered?'center':'left');
  }else{
   if(cl.includes('heading-')){const left=cl.includes('asis')?10:530;const width=cl.includes('asis')?490:700;shape(s,'rect',ox+left*sc,oy+10*sc,width*sc,49*sc,cl.includes('asis')?'#656566':C.brown);continue;}
   const d=a.d||'';const nums=d.match(/-?\d+(?:\.\d+)?/g)?.map(Number)||[];
   if(nums.length<3)continue;let x=nums[0],y=nums[1],endx=x,endy=y;
   if(d.includes('H'))endx=nums[2];else if(d.includes('V'))endy=nums[2];else continue;
   const col=cl.includes('svc')?'#556C85':cl.includes('mgmt')?'#84718E':cl.includes('bk')?'#A87438':a.stroke||C.brown;
   shape(s,'rect',ox+Math.min(x,endx)*sc,oy+Math.min(y,endy)*sc,Math.max(2,Math.abs(endx-x)*sc),Math.max(2,Math.abs(endy-y)*sc),col);
  }
 }
 s.speakerNotes.text+='\n논리 구성도입니다. 물리 포트·Bond 및 Master 실제 구성은 확정 전입니다. 외부 Bastion의 장비 출처 및 내부 잔여 HV 용도는 확인이 필요합니다.';
}
// Preserve every source table row as editable native tables; divide dense tables.
let tableIndex=0;
for(const section of html.matchAll(/<section id="([^"]+)">([\s\S]*?)<\/section>/g)){
 const body=section[2],sectionTitle=clean(body.match(/<h2>(.*?)<\/h2>/)?.[1]||section[1]).replace(/^\d+\.\s*/,'');
 let precedingTitle=sectionTitle,last=0;
 for(const match of body.matchAll(/<table>[\s\S]*?<\/table>/g)){
  const prefix=body.slice(last,match.index),hs=[...prefix.matchAll(/<h3>(.*?)<\/h3>/g)];if(hs.length)precedingTitle=clean(hs.at(-1)[1]);
  last=match.index+match[0].length;
  const rows=[...match[0].matchAll(/<tr>([\s\S]*?)<\/tr>/g)].map(r=>[...r[1].matchAll(/<t[hd][^>]*>([\s\S]*?)<\/t[hd]>/g)].map(c=>clean(c[1])));
  const n=rows[0].length;const widths=n===2?[320,1152]:n===3?[255,615,602]:n===5?[125,175,340,220,612]:Array(n).fill(1472/n);
  const per=n>=5?4:3;
  for(let pos=1;pos<rows.length;pos+=per){const chunk=[rows[0],...rows.slice(pos,pos+per)];const pages=Math.ceil((rows.length-1)/per),page=Math.floor((pos-1)/per)+1;
   const s=slide(precedingTitle+(pages>1?` (${page}/${pages})`:''),sectionTitle===precedingTitle?'':sectionTitle);nativeTable(s,chunk,widths,190,560,n>=5?21:24);
   s.speakerNotes.text+='\n'+clean(body.replace(/<svg[\s\S]*?<\/svg>/g,''));
  }tableIndex++;
 }
}
{const s=slide('설계 확인 및 원본 보관 기준');const lines=['외부 Bastion의 장비 출처와 내부 HV#02·HV#03의 역할을 확인합니다.','Master의 실제 노드 수와 HA 구성, 초기 Worker1 수용 능력을 확인합니다.','IP 상세정보는 국데터 SGIS 구성을 참조합니다.','원본 VMFS는 이관 및 원복 보관 기준 충족 후 회수합니다.','MTV 완료뿐 아니라 업무·DB 통신·백업 정상 여부를 확인합니다.'];lines.forEach((t,i)=>text(s,`${i+1}. ${t}`,80,200+i*100,1420,80,28));}
await fs.writeFile(path.join(build,'table-owners.json'),JSON.stringify(tableOwners));
await (await PresentationFile.exportPptx(p)).save(path.join(build,'candidate.pptx'));
await fs.writeFile(path.join(build,'deck.json'),JSON.stringify(p.toProto()));
for(let i=0;i<p.slides.items.length;i++){const blob=await p.export({slide:p.slides.items[i],format:'png',scale:1});await fs.writeFile(path.join(build,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));console.log('Rendered '+(i+1));}
console.log('SLIDES='+p.slides.items.length+' TABLES='+tableIndex);
