import React from "react";
import { Composition } from "remotion";
import { Video } from "./Video";
import { Preview } from "./Preview";
import T from "./timeline.json";
export const Root: React.FC = () => (
  <>
  <Composition id="Preview" component={Preview} durationInFrames={60} fps={30} width={1080} height={1920} />
  <Composition id="Video" component={Video} durationInFrames={T.total} fps={T.fps} width={1080} height={1920} defaultProps={{ withAudio: false }} />
  </>
);
