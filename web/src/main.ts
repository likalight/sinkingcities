import * as maplibregl from 'maplibre-gl';
import type * as GeoJSON from 'geojson';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';
import 'maplibre-gl/dist/maplibre-gl.css';
import './style.css';

type City = {city:string; name:string; bbox:number[]; queried_at:string; catalog_count:number; search_complete:boolean; chain_pairs:number; selected_group:(string|number)[]|null; start:string|null; end:string|null; measurement_status:string};
type Footprint = {type:'Feature'; geometry:GeoJSON.Geometry; properties:{city:string; scene:string; track:number; frame:number; direction:string; start:string; end:string; maturity:string; selected:boolean; url:string}};
type Catalog = {type:'FeatureCollection'; features:Footprint[]};
const root = document.querySelector<HTMLDivElement>('#app')!;
const base = import.meta.env.BASE_URL;
maplibregl.setWorkerUrl(workerUrl);
const sources = [
  ['NISAR L2 GUNW · ASF DAAC','https://nisar-docs.asf.alaska.edu/gunw/','Used: real granule metadata, acquisition dates and geographic footprints. No phase arrays processed yet.'],
  ['NASA / IPCC AR6 projections','https://sealevel.nasa.gov/data_tools/17/','Planned: coastal sea-level scenarios. No projection values are loaded.'],
  ['NASADEM · NASA Earthdata','https://www.earthdata.nasa.gov/data/catalog/lpcloud-nasadem-hgt-001','Planned: terrain context. No elevation or inundation result is shown.'],
  ['Jakarta subsidence research','https://piahs.copernicus.org/articles/372/115/2015/','Literature context: historical measurements are not our 2026 results.'],
];
const steps = [
  ['See through the clouds','Radar can observe surface change through cloud cover. NISAR’s L-band offers sensitivity to ground motion, but atmosphere, vegetation changes and water still complicate interferometry.'],
  ['First, check the evidence','These footprints and acquisition dates come from the live ASF catalog. A scene intersecting a city does not guarantee coherent pixels or a continuous time series.'],
  ['Measure motion carefully','Next: inspect the HDF5 product, mask poor coherence, apply ionospheric correction and reference each pair to a justified stable area. LOS displacement is not vertical subsidence.'],
  ['Explore 2050 responsibly','A future scenario can combine sea-level change with continued subsidence. Align the time baseline and account for any land-motion component already included in AR6. This would be a scenario, not a flood prediction.'],
  ['Turn evidence into action','Use validated measurements to prioritize monitoring and investigate groundwater management. Confirm results with longer time series and independent ground measurements before local decisions.'],
];

async function getJSON<T>(name:string):Promise<T> {
  const response = await fetch(`${base}data/${name}`);
  if (!response.ok) throw new Error(`Could not load ${name}`);
  return response.json() as Promise<T>;
}

async function main() {
  const [cities, catalog] = await Promise.all([getJSON<City[]>('coverage.json'), getJSON<Catalog>('footprints.geojson')]);
  let current = cities.find(c=>c.city==='semarang') ?? cities[0];
  let map:maplibregl.Map|undefined;
  let story = 0;
  root.innerHTML = `
    <header><a class="brand" href="#"><span class="brand-icon" aria-hidden="true">≋</span>Sinking<span>Cities</span></a><span class="header-note">SOUTHEAST ASIA / COASTAL CHANGE OBSERVATORY</span><button id="about-open" class="quiet">About the data ↗</button></header>
    <main>
      <section class="intro"><div><p class="eyebrow">NASA SPACE APPS 2026 · RESEARCH PROTOTYPE</p><h1>When the land sinks,<br>the sea gets closer.</h1><p class="lede">Watching coastal cities change from orbit.<br>Start with the evidence. Make the uncertainty visible.</p></div><div class="status"><span class="status-dot"></span><div><strong>Coverage verified. Motion not yet measured.</strong><p>Real NASA catalog data · no simulated subsidence</p></div></div></section>
      <section class="workspace" aria-label="NISAR coverage explorer">
        <aside class="sidebar"><div class="section-label">01 / EXPLORE A CITY</div><label for="city">Study region</label><select id="city">${cities.map(c=>`<option value="${c.city}">${c.name}</option>`).join('')}</select><p id="city-note" class="small"></p>
          <div class="metrics"><div><strong id="count"></strong><span>catalog granules</span></div><div><strong id="chain"></strong><span>consecutive pairs¹</span></div></div>
          <p id="range" class="range"></p><div id="group" class="small"></div>
          <div class="divider"></div><div class="section-label">02 / MAP LAYERS</div>
          <label class="check"><input id="footprints" type="checkbox" checked>NASA acquisition footprints</label><label class="check"><input id="aoi" type="checkbox" checked>Study area</label>
          <fieldset disabled><legend>Awaiting verified processing</legend><label class="check"><input type="checkbox">Subsidence velocity · cm/yr</label><label class="check"><input type="checkbox">Coherence / uncertainty</label><label class="check"><input type="checkbox">Relative sea-level scenario · 2050</label></fieldset>
          <p class="small footnote">¹ Longest 12-day chain covering ≥99% of the search box, within one compatible product group. Footprint coverage does not establish data quality.</p><a id="report" class="text-link">Read coverage report ↗</a>
        </aside>
        <div class="map-column"><div class="map-bar"><span><i class="dot"></i>LIVE CATALOG SNAPSHOT</span><span id="asof"></span></div><div id="map" aria-label="Interactive map of NISAR acquisition footprints"></div><div class="map-key"><span><i class="key-aoi"></i>Study area</span><span><i class="key-footprint"></i>Catalog footprint</span><span>Click a footprint for its source record</span></div><p id="map-message" role="status"></p></div>
        <aside class="inspector"><div class="section-label">03 / INSPECT THE EVIDENCE</div><h2 id="inspect-title">A measurement starts<br>with a usable pair.</h2><div id="record"><p class="muted">Select a footprint on the map to inspect its acquisition dates and provenance.</p></div><div class="chart-empty"><span aria-hidden="true">⌁</span><strong>Displacement chart pending</strong><p>Authenticated radar arrays and a validated reference are required. No rate or uncertainty is available yet.</p></div><div class="next"><span class="eyebrow">NEXT SCIENCE GATE</span><h3>Inspect one real granule.</h3><p>Confirm phase, coherence, connected components, ionosphere, wavelength and projection before calculating displacement.</p></div></aside>
      </section>
      <section class="story"><div><p class="eyebrow">THE BIGGER PICTURE</p><h2>Rising water is only<br>half the story.</h2></div><div class="story-content"><span id="story-count" class="eyebrow"></span><h3 id="story-title"></h3><p id="story-text"></p><div class="story-controls"><button id="prev" class="quiet">← Previous</button><button id="next">Next chapter →</button></div></div></section>
      <footer><span>NASA–ISRO radar. Local questions. Traceable evidence.</span><span>Code assisted by OpenAI Codex · Prototype, not a flood forecast</span></footer>
    </main>
    <dialog id="about"><div class="dialog-top"><p class="eyebrow">PROVENANCE & LIMITATIONS</p><button id="about-close" class="quiet" aria-label="Close data panel">Close ×</button></div><h2>What the data can tell us.</h2><p>This version uses NASA catalog metadata to assess whether a subsidence time series is feasible. It does not yet demonstrate measured surface change.</p>${sources.map(s=>`<article><h3><a href="${s[1]}" target="_blank" rel="noopener noreferrer">${s[0]} ↗</a></h3><p>${s[2]}</p></article>`).join('')}<article><h3>Limits that matter</h3><p>No coherence mask, ionospheric correction, stable reference, measured velocity, DEM or sea-level projection has been applied in this prototype. No GNSS ground truth is available. Raw product access requires NASA Earthdata authentication.</p><p>The available continuous chain can be much shorter than the mission date span. Single-orbit LOS motion cannot be called vertical subsidence without an explicit approximation. Residual scatter and velocity uncertainty require different units and labels.</p><p>Basemap: © OpenStreetMap contributors. Basemap data are a non-NASA complement.</p></article></dialog>`;
  const el = <T extends HTMLElement=HTMLElement>(id:string)=>document.getElementById(id) as T;
  const dialog = el<HTMLDialogElement>('about');
  el('about-open').onclick=()=>dialog.showModal();
  el('about-close').onclick=()=>dialog.close();
  dialog.addEventListener('click', e=>{if(e.target===dialog) dialog.close();});
  const aoiData = (city:City):GeoJSON.FeatureCollection => {const [w,s,e,n]=city.bbox;return {type:'FeatureCollection',features:[{type:'Feature',properties:{},geometry:{type:'Polygon',coordinates:[[[w,s],[e,s],[e,n],[w,n],[w,s]]]}}]};};
  function update() {
    el<HTMLSelectElement>('city').value=current.city;
    el('count').textContent=String(current.catalog_count);
    el('chain').textContent=String(current.chain_pairs);
    el('range').textContent=current.start?`${current.start} → ${current.end}`:'No full-box chain selected';
    el('group').textContent=current.selected_group?`${current.selected_group[0]} · Track ${current.selected_group[1]} / frame ${current.selected_group[2]} · ${String(current.selected_group[3]).toLowerCase()}`:'Intersections exist; inspect smaller areas or frame coverage.';
    el('city-note').textContent=current.city==='semarang'?'First inspection candidate · coherence not assessed':current.city==='jakarta'?'Primary research target · broad box crosses frames':'Backup study region · coherence not assessed';
    el('asof').textContent=`${new Date(current.queried_at).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric',timeZone:'Asia/Singapore'})}`;
    el<HTMLAnchorElement>('report').href=`${base}data/coverage_${current.city}.md`;
    el('record').textContent='Select a footprint to inspect its dates and source. No displacement values are available.';
    if(map?.getSource('footprints')) {
      (map.getSource('footprints') as maplibregl.GeoJSONSource).setData({type:'FeatureCollection',features:catalog.features.filter(f=>f.properties.city===current.city)});
      (map.getSource('aoi') as maplibregl.GeoJSONSource).setData(aoiData(current));
      const [w,s,e,n]=current.bbox; map.fitBounds([[w,s],[e,n]],{padding:60,duration:700});
    }
  }
  el<HTMLSelectElement>('city').onchange=e=>{current=cities.find(c=>c.city===(e.target as HTMLSelectElement).value)!;update();};
  function setStory() {el('story-count').textContent=`${String(story+1).padStart(2,'0')} / 05`;el('story-title').textContent=steps[story][0];el('story-text').textContent=steps[story][1];el<HTMLButtonElement>('prev').disabled=story===0;el<HTMLButtonElement>('next').disabled=story===steps.length-1;}
  el('prev').onclick=()=>{story--;setStory();};el('next').onclick=()=>{story++;setStory();};setStory();update();
  try {
    map = new maplibregl.Map({container:'map',style:{version:8,sources:{basemap:{type:'raster',tiles:['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],tileSize:256,maxzoom:19,attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}},layers:[{id:'basemap',type:'raster',source:'basemap',paint:{'raster-saturation':-0.7,'raster-opacity':0.85}}]},center:[110.4,-6.97],zoom:10});
    map.addControl(new maplibregl.NavigationControl({showCompass:false}),'top-right');
    map.addControl(new maplibregl.ScaleControl({unit:'metric'}));
    map.on('error',()=>{el('map-message').textContent='Some map resources could not load. Coverage totals and source reports remain available.';});
    map.on('load',()=>{
      map!.addSource('footprints',{type:'geojson',data:{type:'FeatureCollection',features:[]}});
      map!.addLayer({id:'footprint-fill',type:'fill',source:'footprints',paint:{'fill-color':'#247f8a','fill-opacity':0.035}});
      map!.addLayer({id:'footprint-line',type:'line',source:'footprints',paint:{'line-color':'#247f8a','line-width':1,'line-opacity':0.6}});
      map!.addSource('aoi',{type:'geojson',data:aoiData(current)});
      map!.addLayer({id:'aoi-line',type:'line',source:'aoi',paint:{'line-color':'#bb5d38','line-width':2,'line-dasharray':[3,2]}});
      map!.on('click','footprint-fill',event=>{
        const p = event.features?.[0]?.properties; if(!p)return;
        el('inspect-title').textContent='Inside the catalog';
        const box = el('record');box.replaceChildren();
        const badge=document.createElement('span');badge.className='record-badge';badge.textContent=String(p.maturity);box.append(badge);
        for(const [label,value] of [['Reference',p.start],['Secondary',p.end],['Orbit',`${p.direction} · track ${p.track}`],['Frame',p.frame]]) {const line=document.createElement('p');line.className='record-row';const title=document.createElement('span');title.textContent=String(label);const val=document.createElement('strong');val.textContent=String(value);line.append(title,val);box.append(line);}
        const name=document.createElement('p');name.className='scene-name';name.textContent=String(p.scene);box.append(name);
        const link=document.createElement('a');link.href=String(p.url);link.textContent='NASA product ↗ (Earthdata login)';link.target='_blank';link.rel='noopener noreferrer';link.className='text-link';box.append(link);
      });
      for(const [control,layers] of [['footprints',['footprint-fill','footprint-line']],['aoi',['aoi-line']]] as const) el<HTMLInputElement>(control).onchange=()=>layers.forEach(id=>map!.setLayoutProperty(id,'visibility',el<HTMLInputElement>(control).checked?'visible':'none'));
      update();
    });
  } catch {el('map-message').textContent='Interactive mapping is unavailable in this browser. Use the city selector and coverage reports to inspect the evidence.';}
}
main().catch(()=>{root.innerHTML='<main class="fatal"><h1>Coverage data could not load.</h1><p>Check the connection and reload. No measurements will be substituted.</p><button onclick="location.reload()">Reload</button></main>';});
