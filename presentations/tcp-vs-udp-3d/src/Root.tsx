import React from "react";
import { Composition } from "remotion";
import { Video } from "./Video";
import { FPS, TOTAL } from "./timing";
export const Root: React.FC = () => <Composition id="Video" component={Video} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080} defaultProps={{ withAudio: false }} />;
