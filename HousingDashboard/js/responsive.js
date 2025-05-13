function scaleDash(){
    const baseWidth = 1536; //mine as the base (adjusted css for it)
    const baseHeight = 729.6;
    const screenW = window.innerWidth;
    const screenH = window.innerHeight;
    const scaleX = screenW / baseWidth; //find ratio
    const scaleY = screenH / baseHeight;
    const minScale = Math.min(1024 / baseWidth, 600 / baseHeight);  //smallest laptop/desktop sizes (common)
    const finalScaleX = Math.max(minScale, scaleX); //just in case theres something smaller (breaks below 1024)
    const finalScaleY = Math.max(minScale, scaleY);
    const app = document.getElementById('app');

    app.style.transform = `scale(${finalScaleX}, ${finalScaleY})`;
    app.style.transformOrigin = "top left";
    app.style.width = `${baseWidth}px`;
    app.style.height = `${baseHeight}px`;
    app.style.position = "absolute";
    app.style.top = "0";    //exact
    app.style.left = "0";
}
window.addEventListener("load", scaleDash);
window.addEventListener("resize", scaleDash);