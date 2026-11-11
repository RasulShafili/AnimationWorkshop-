import React from "react";
import { Composition } from "remotion";
import { Video } from "./Video";
import T from "./timeline.json";
export const Root: React.FC = () => <Composition id="Video" component={Video} durationInFrames={T.total} fps={T.fps} width={1080} height={1920} defaultProps={{ withAudio: false }} />;
