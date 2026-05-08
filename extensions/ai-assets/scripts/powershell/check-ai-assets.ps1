param(
    [switch]$Json,
    [string]$Root = ".",
    [string]$FeatureDir = ""
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$checkScript = Join-Path $scriptDir "..\check_ai_assets.py"
$resolvedRoot = (Resolve-Path $Root).Path

if ($FeatureDir -ne "") {
    $resolvedFeature = (Resolve-Path $FeatureDir).Path
    python $checkScript $resolvedRoot --feature-dir $resolvedFeature
} else {
    python $checkScript $resolvedRoot
}
