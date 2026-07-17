import { Particles, ParticlesProvider } from '@tsparticles/react'
import { loadSlim } from '@tsparticles/slim'
const initParticles = async engine => { await loadSlim(engine) }
const options = { fullScreen:{enable:false}, fpsLimit:60, interactivity:{events:{onClick:{enable:false},onHover:{enable:false}}}, particles:{color:{value:['#7048E8','#FF6B5B']},links:{enable:false},move:{enable:true,speed:0.35,outModes:{default:'out'}},number:{value:40,density:{enable:true}},opacity:{value:{min:0.42,max:0.55}},shape:{type:'circle'},size:{value:{min:2,max:5}}},detectRetina:true }
export default function AmbientParticles({ id }) { return <ParticlesProvider init={initParticles}><Particles id={id} className="hero-particles" options={options}/></ParticlesProvider> }
