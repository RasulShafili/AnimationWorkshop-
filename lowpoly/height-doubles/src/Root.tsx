import React from "react";
import { Composition } from "remotion";
import { Video } from "./Video";
import { FPS, TOTAL } from "./timeline";
export const Root: React.FC = () => (
  <>
    <Composition id="Video" component={Video} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} defaultProps={{ withAudio: false, pixel: false }} />
    <Composition id="Pixel" component={Video} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} defaultProps={{ withAudio: false, pixel: true }} />
  </>
);
