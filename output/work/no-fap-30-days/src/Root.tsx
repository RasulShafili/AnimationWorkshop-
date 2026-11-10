import React from "react";
import { Composition } from "remotion";
import { MainVideo } from "./MainVideo";
import { SceneRenderer } from "./SceneRenderer";
import timingData from "../audio/timing.json";

export const Root: React.FC = () => {
  return (
    <>
      {/* Final Production Composition */}
      <Composition
        id="Main"
        component={MainVideo}
        durationInFrames={timingData.totalFrames}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          showDebug: false
        }}
      />

      {/* Phase 1 Setup Test Composition */}
      <Composition
        id="Test"
        component={() => (
          <div
            style={{
              width: 1080,
              height: 1920,
              backgroundColor: "#1a1226",
              color: "#ffd93b",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: 64,
              fontFamily: "monospace"
            }}
          >
            TEST
          </div>
        )}
        durationInFrames={30}
        fps={30}
        width={1080}
        height={1920}
      />

      {/* Phase 5a Scene 3 Key Scene 6s Test */}
      <Composition
        id="Scene3Test"
        component={() => (
          <SceneRenderer
            sceneId={3}
            localFrame={60}
            durationFrames={180}
            globalFrame={260}
            showDebug={true}
          />
        )}
        durationInFrames={180}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
