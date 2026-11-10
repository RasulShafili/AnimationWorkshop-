import { Config } from "@remotion/cli/config";
// PNG intermediates: JPEG would smear the dither pattern before the final encode.
Config.setVideoImageFormat("png");
Config.setCodec("h264");
Config.setCrf(16);
Config.setOverwriteOutput(true);
