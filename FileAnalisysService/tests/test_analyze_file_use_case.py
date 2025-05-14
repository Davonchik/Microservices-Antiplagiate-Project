import hashlib
import re
from uuid import uuid4, UUID

import pytest

from app.domain.entities.models import FileAnalysisModel
from app.domain.exceptions.exceptions import FileNotFoundException

def test_execute_creates_new_analysis(analyze_use_case):
    use_case, repo, file_map, tmp = analyze_use_case
    fid = uuid4()
    text = "Para1\n\nPara2 line1\nPara2 line2"
    data = text.encode("utf-8")
    file_map[fid] = data

    result: FileAnalysisModel = use_case.execute(fid)

    assert result.file_id == fid
    assert result.paragraphs_count == 2
    assert result.words_count == len(text.split())
    assert result.symbols_count == len(text)

    expected_hash = hashlib.sha256(data).hexdigest()
    assert result.content_hash == expected_hash

    img_path = tmp / "wordclouds" / f"{fid}.svg"
    assert img_path.exists()
    assert img_path.read_bytes() == b"IMGBYTES"

    assert len(repo.saved) == 1
    assert repo.saved[0] is result

def test_execute_returns_existing_for_same_hash(analyze_use_case):
    use_case, repo, file_map, _ = analyze_use_case
    fid1, fid2 = uuid4(), uuid4()
    data = b"dupcontent"
    file_map[fid1] = data
    file_map[fid2] = data

    first = use_case.execute(fid1)
    second = use_case.execute(fid2)

    assert second is first
    assert len(repo.saved) == 1

def test_execute_raises_missing_file(analyze_use_case):
    use_case, _, file_map, _ = analyze_use_case
    missing = uuid4()
    
    with pytest.raises(FileNotFoundException):
        use_case.execute(missing)

def test_execute_propagates_wordcloud_error(analyze_use_case):
    use_case, repo, file_map, _ = analyze_use_case
    
    use_case.wordcloud = type(use_case.wordcloud)(fail=True)
    fid = uuid4()
    file_map[fid] = b"X"
    with pytest.raises(Exception) as ei:
        use_case.execute(fid)
    assert "WC ERROR" in str(ei.value)
    assert repo.saved == []