// 3D pixel look: the scene renders at 270x480, then a post pass posterizes with a 4x4 Bayer dither.
import { useMemo } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";
import { RenderPass } from "three/examples/jsm/postprocessing/RenderPass.js";
import { ShaderPass } from "three/examples/jsm/postprocessing/ShaderPass.js";
import { OutputPass } from "three/examples/jsm/postprocessing/OutputPass.js";

const Dither = {
  uniforms: { tDiffuse: { value: null }, levels: { value: 7.0 } },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: `
    uniform sampler2D tDiffuse; uniform float levels; varying vec2 vUv;
    float bayer4(vec2 p){
      int x = int(mod(p.x, 4.0)), y = int(mod(p.y, 4.0)); int i = x + y * 4;
      float m[16] = float[16](0.,8.,2.,10.,12.,4.,14.,6.,3.,11.,1.,9.,15.,7.,13.,5.);
      return (m[i] + 0.5) / 16.0;
    }
    void main(){
      vec3 c = texture2D(tDiffuse, vUv).rgb;
      float b = (bayer4(floor(gl_FragCoord.xy)) - 0.5) * 0.9;
      vec3 q = floor(c * levels + b + 0.5) / levels;
      gl_FragColor = vec4(clamp(q, 0.0, 1.0), 1.0);
    }`,
};

export const PixelPost: React.FC = () => {
  const { gl, scene, camera, size } = useThree();
  const composer = useMemo(() => {
    const c = new EffectComposer(gl);
    c.setPixelRatio(1); c.setSize(size.width, size.height);
    c.addPass(new RenderPass(scene, camera)); c.addPass(new OutputPass()); c.addPass(new ShaderPass(Dither));
    return c;
  }, [gl, scene, camera, size.width, size.height]);
  useFrame(() => composer.render(), 1); // priority > 0: we own the final render
  return null;
};
