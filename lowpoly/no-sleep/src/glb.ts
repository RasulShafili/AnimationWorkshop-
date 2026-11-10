// Load GLB files before the canvas renders, so Remotion's frame capture always includes the models.
import { useEffect, useState } from "react";
import { staticFile, delayRender, continueRender } from "remotion";
import { GLTFLoader, GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";

const cache = new Map<string, Promise<GLTF>>();
export const loadGLB = (file: string) => {
  if (!cache.has(file)) cache.set(file, new Promise((res, rej) => new GLTFLoader().load(staticFile(file), res, undefined, rej)));
  return cache.get(file)!;
};
export const useGLBs = (files: string[]) => {
  const [data, setData] = useState<Record<string, GLTF> | null>(null);
  const [h] = useState(() => delayRender("glb " + files.join(",")));
  useEffect(() => {
    Promise.all(files.map(loadGLB)).then(list => { const o: Record<string, GLTF> = {}; files.forEach((f, i) => (o[f] = list[i])); setData(o); })
      .catch(e => { console.error("GLB load failed", e); });
  }, []);
  useEffect(() => { if (data) continueRender(h); }, [data]);
  return data;
};
