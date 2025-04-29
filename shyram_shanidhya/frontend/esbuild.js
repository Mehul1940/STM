import path from "node:path";

import * as esbuild from "esbuild";
import { sassPlugin } from "esbuild-sass-plugin";

const __dirname = import.meta.dirname;

const ctx = await esbuild.context({
  entryPoints: [path.resolve(__dirname, "js", "index.js")],

  bundle: true,
  plugins: [sassPlugin()],
  outdir: path.resolve(__dirname, "../", "static"),
});

await ctx.watch();
console.log("watching...");
