// Post chain: render → gravitational lens (screen space, around the black hole) → bloom → output.
// World writes LENS each frame (screen position + Einstein radius in px); this reads it before rendering.
import { useMemo } from "react";
import * as THREE from "three";
import { useFrame, useThree } from "@react-three/fiber";
import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";
import { RenderPass } from "three/examples/jsm/postprocessing/RenderPass.js";
import { ShaderPass } from "three/examples/jsm/postprocessing/ShaderPass.js";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/examples/jsm/postprocessing/OutputPass.js";

export const LENS = { on: 0, x: 540, y: 960, re: 80 };
const LensShader = {
  uniforms: { tDiffuse: { value: null }, uC: { value: new THREE.Vector2() }, uRe: { value: 80 }, uOn: { value: 0 }, uRes: { value: new THREE.Vector2(1080, 1920) } },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: `
    uniform sampler2D tDiffuse; uniform vec2 uC, uRes; uniform float uRe, uOn; varying vec2 vUv;
    void main() {
      vec2 p = vUv * uRes; vec2 d = p - uC; float r = max(length(d), 0.001);
      if (uOn < 0.5) { gl_FragColor = texture2D(tDiffuse, vUv); return; }
      float shadow = uRe * 0.52;
      // lens equation (point mass): source radius = r - Re^2 / r
      float rs = r - uRe * uRe / r;
      vec2 q = uC + d / r * rs;
      vec3 col = texture2D(tDiffuse, clamp(q / uRes, 0.0, 1.0)).rgb;
      // magnification brightens the ring a little
      float mag = clamp(1.0 + 0.35 * exp(-pow((r - uRe) / (uRe * 0.18), 2.0)), 1.0, 1.5);
      col *= mag;
      // the shadow and a thin photon ring
      float ring = exp(-pow((r - shadow * 1.04) / (shadow * 0.035), 2.0));
      col = mix(vec3(0.0), col, smoothstep(shadow * 0.98, shadow * 1.02, r)) + vec3(1.0, 0.85, 0.6) * ring * 0.9;
      gl_FragColor = vec4(col, 1.0);
    }`,
};
export const LensPost: React.FC = () => {
  const { gl, scene, camera, size } = useThree();
  const { composer, lens } = useMemo(() => {
    gl.toneMapping = THREE.ACESFilmicToneMapping; gl.toneMappingExposure = 1.05;
    const rt = new THREE.WebGLRenderTarget(size.width, size.height, { type: THREE.HalfFloatType, samples: 4 });
    const c = new EffectComposer(gl, rt); c.setPixelRatio(1); c.setSize(size.width, size.height);
    c.addPass(new RenderPass(scene, camera));
    const l = new ShaderPass(LensShader); c.addPass(l);
    c.addPass(new UnrealBloomPass(new THREE.Vector2(size.width / 2, size.height / 2), 0.7, 0.55, 0.85));
    c.addPass(new OutputPass());
    return { composer: c, lens: l };
  }, [gl, scene, camera, size.width, size.height]);
  useFrame(() => {
    const u = lens.uniforms; u.uOn.value = LENS.on; u.uC.value.set(LENS.x, 1920 - LENS.y); u.uRe.value = LENS.re;
    composer.render();
  }, 1);
  return null;
};
