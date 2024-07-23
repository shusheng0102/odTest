以下是对这段 Python 代码的详细解释：

```python
class PretrainedFSMTModel(PreTrainedModel):
```

定义了一个名为 `PretrainedFSMTModel` 的类，它继承自 `PreTrainedModel` 。

```python
    config_class = FSMTConfig
    base_model_prefix = "model"
```

指定了模型的配置类为 `FSMTConfig` ，并定义了基础模型的前缀为 `"model"` 。

```python
    def _init_weights(self, module):
        std = self.config.init_std
        if isinstance(module, nn.Linear):
            module.weight.data.normal_(mean=0.0, std=std)
            if module.bias is not None:
                module.bias.data.zero_()
        elif isinstance(module, SinusoidalPositionalEmbedding):
            pass
        elif isinstance(module, nn.Embedding):
            module.weight.data.normal_(mean=0.0, std=std)
            if module.padding_idx is not None:
                module.weight.data[module.padding_idx].zero_()
```

定义了一个名为 `_init_weights` 的方法，用于初始化模型的权重。根据模块的类型（如线性层、嵌入层等）进行不同的初始化操作。对于线性层，权重采用正态分布初始化，均值为 0，标准差为 `self.config.init_std` ，偏置若存在则置零。对于嵌入层也进行类似的初始化，并对填充索引对应的权重置零。对于 `SinusoidalPositionalEmbedding` 类型则不进行操作。

```python
    @property
    def dummy_inputs(self):
        pad_token = self.config.pad_token_id
        input_ids = torch.tensor([[0, 6, 10, 4, 2], [0, 8, 12, 2, pad_token]], device=self.device)
        dummy_inputs = {
            "attention_mask": input_ids.ne(pad_token),
            "input_ids": input_ids,
        }
        return dummy_inputs
```

定义了一个属性方法 `dummy_inputs` ，用于生成一些示例输入数据。它根据模型配置中的填充标记 `pad_token_id` 创建了输入 ID 的张量，并构建了包含注意力掩码和输入 ID 的字典作为示例输入返回。


以下是对这段 Python 代码的详细解释：

```python
def invert_mask(attention_mask):
    """Turns 1->0, 0->1, False->True, True-> False"""
    assert attention_mask.dim() == 2
    return attention_mask.eq(0)
```

这个函数用于反转注意力掩码。它要求输入的 `attention_mask` 是二维的，并返回一个新的掩码，其中原掩码中的 1 变为 0，0 变为 1，`True` 变为 `False`，`False` 变为 `True` 。

```python
def triu_onnx(x, diagonal=0):
    l = x.shape[0]
    arange = torch.arange(l, device=x.device)
    mask = arange.expand(l, l)
    arange = arange.unsqueeze(-1)
    if diagonal:
        arange = arange + diagonal
    mask = mask >= arange
    return x.masked_fill(mask == 0, 0)
```

这个函数创建一个上三角掩码，并将输入 `x` 中对应掩码为 0 的位置填充为 0 。可以通过 `diagonal` 参数控制上三角的偏移。

```python
def _prepare_fsmt_decoder_inputs(
    config,
    input_ids,
    decoder_input_ids=None,
    decoder_padding_mask=None,
    causal_mask_dtype=torch.float32,
):
    """
    Prepare masks that ignore padding tokens in the decoder and a causal mask for the decoder if none are provided.
    This mimics the default behavior in fairseq. To override it pass in masks. Note: this is not called during
    generation
    """
    pad_token_id = config.pad_token_id
    if decoder_input_ids is None:
        decoder_input_ids = shift_tokens_right(input_ids, pad_token_id)
    bsz, tgt_len = decoder_input_ids.size()
    if decoder_padding_mask is None:
        decoder_padding_mask = make_padding_mask(decoder_input_ids, pad_token_id)
    else:
        decoder_padding_mask = invert_mask(decoder_padding_mask)
    causal_mask = triu_onnx(fill_with_neg_inf(torch.zeros(tgt_len, tgt_len)), 1).to(
        dtype=causal_mask_dtype, device=decoder_input_ids.device
    )
    return decoder_input_ids, decoder_padding_mask, causal_mask
```

这个函数用于准备 FSMT 解码器的输入。如果没有提供解码器的输入 ID 和填充掩码，它会进行相应的默认处理。具体来说，如果 `decoder_input_ids` 为空，会根据 `input_ids` 和填充标记进行处理得到；如果 `decoder_padding_mask` 为空，会创建一个；否则，反转传入的填充掩码。最后创建一个上三角的因果掩码，并返回处理后的解码器输入 ID、填充掩码和因果掩码。



在 PyTorch 中，可以使用 `torch.nn.DataParallel` 来实现数据并行训练。以下是一个简单的示例代码：

```python
import torch
import torch.nn as nn

# 定义模型
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.layer1 = nn.Linear(100, 200)
        self.layer2 = nn.Linear(200, 50)
        self.output_layer = nn.Linear(50, 10)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        return self.output_layer(x)

model = MyModel()

# 如果有多个 GPU 可用
if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)

# 定义损失函数和优化器
loss_func = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 模拟数据
x = torch.randn(100, 100).cuda()  # 如果有 GPU
y = torch.randint(0, 10, (100,)).cuda()  # 如果有 GPU

# 训练循环
for epoch in range(10):
    optimizer.zero_grad()
    outputs = model(x)
    loss = loss_func(outputs, y)
    loss.backward()
    optimizer.step()
```

在上述代码中：

1. 首先定义了一个简单的模型 `MyModel` 。
2. 如果有多个 GPU 可用，通过 `nn.DataParallel` 对模型进行包装，实现数据并行。
3. 定义了损失函数和优化器。
4. 准备数据并在训练循环中进行前向传播、计算损失、反向传播和参数更新。

需要注意的是，使用 `DataParallel` 时，模型会被复制到多个 GPU 上，数据会被自动分割并在多个 GPU 上并行计算。


以下是对这段代码的详细解释：

```python
def _make_linear_from_emb(emb):
    """
    从给定的嵌入层创建一个线性层。

    参数：
    emb：嵌入层

    返回：
    一个新的线性层，其权重与嵌入层的权重相同
    """
    vocab_size, emb_size = emb.weight.shape
    lin_layer = nn.Linear(vocab_size, emb_size, bias=False)
    lin_layer.weight.data = emb.weight.data
    return lin_layer
```

```python
def _check_shapes(shape_1, shape2):
    """
    检查两个形状是否匹配，如果不匹配则引发断言错误。

    参数：
    shape_1：第一个形状
    shape2：第二个形状
    """
    if shape_1!= shape2:
        raise AssertionError(f"shape mismatch: {shape_1}!= {shape2}")
```

```python
def shift_tokens_right(input_ids, pad_token_id):
    """
    将输入的 ID 向右移动一个标记，并包裹最后一个非填充标记（通常是 <eos>）。

    参数：
    input_ids：输入的标记 ID
    pad_token_id：填充标记的 ID

    返回：
    移动后的标记 ID
    """
    prev_output_tokens = input_ids.clone()
    index_of_eos = (input_ids.ne(pad_token_id).sum(dim=1) - 1).unsqueeze(-1)
    prev_output_tokens[:, 0] = input_ids.gather(1, index_of_eos).squeeze()
    prev_output_tokens[:, 1:] = input_ids[:, :-1]
    return prev_output_tokens
```

```python
def make_padding_mask(input_ids, padding_idx=1):
    """
    创建一个填充掩码，其中填充标记为 True。

    参数：
    input_ids：输入的标记 ID
    padding_idx：填充标记的索引（默认值为 1）

    返回：
    一个布尔掩码，如果没有填充标记，则返回 None
    """
    padding_mask = input_ids.eq(padding_idx)
    if not padding_mask.any():
        padding_mask = None
    return padding_mask
```


以下是对这段代码的详细解释：

```python
class EncoderLayer(nn.Module):
```

定义了一个名为 `EncoderLayer` 的类，它继承自 `nn.Module` ，表示这是一个 PyTorch 的模块。

```python
    def __init__(self, config: FSMTConfig):
        super().__init__()
        self.embed_dim = config.d_model
        self.self_attn = Attention(self.embed_dim, config.encoder_attention_heads, dropout=config.attention_dropout)
        self.self_attn_layer_norm = LayerNorm(self.embed_dim)
        self.dropout = config.dropout
        self.activation_fn = ACT2FN[config.activation_function]
        self.activation_dropout = config.activation_dropout
        self.fc1 = nn.Linear(self.embed_dim, config.encoder_ffn_dim)
        self.fc2 = nn.Linear(config.encoder_ffn_dim, self.embed_dim)
        self.final_layer_norm = LayerNorm(self.embed_dim)
```

在初始化方法中，设置了一些属性，包括嵌入维度、自注意力机制、层归一化、Dropout 概率、激活函数等，并定义了两个线性层。

```python
    def forward(self, x, encoder_padding_mask, layer_head_mask, output_attentions=False):
```

定义了前向传播方法。

```python
        residual = x
        x, attn_weights = self.self_attn(
            query=x,
            key=x,
            key_padding_mask=encoder_padding_mask,
            layer_head_mask=layer_head_mask,
            output_attentions=output_attentions,
        )
        x = nn.functional.dropout(x, p=self.dropout, training=self.training)
        x = residual + x
        x = self.self_attn_layer_norm(x)
```

这部分首先保存输入 `x` 作为残差，然后进行自注意力计算，应用 Dropout ，加上残差并进行层归一化。

```python
        residual = x
        x = self.activation_fn(self.fc1(x))
        x = nn.functional.dropout(x, p=self.activation_dropout, training=self.training)
        x = self.fc2(x)
        x = nn.functional.dropout(x, p=self.dropout, training=self.training)
        x = residual + x
        x = self.final_layer_norm(x)
        return x, attn_weights
```

这部分再次保存残差，经过前馈神经网络（包含激活函数、Dropout 等），加上残差并进行最终的层归一化，最后返回输出 `x` 和注意力权重 `attn_weights` 。

以下是对这段代码的详细解释：

```python
class DecoderLayer(nn.Module):
```

定义了一个名为 `DecoderLayer` 的类，它继承自 `nn.Module` 。

```python
    def __init__(self, config: FSMTConfig):
        super().__init__()
        self.embed_dim = config.d_model
        self.self_attn = Attention(
            embed_dim=self.embed_dim,
            num_heads=config.decoder_attention_heads,
            dropout=config.attention_dropout,
        )
        self.dropout = config.dropout
        self.activation_fn = ACT2FN[config.activation_function]
        self.activation_dropout = config.activation_dropout
        self.self_attn_layer_norm = LayerNorm(self.embed_dim)
        self.encoder_attn = Attention(
            self.embed_dim,
            config.decoder_attention_heads,
            dropout=config.attention_dropout,
            encoder_decoder_attention=True,
        )
        self.encoder_attn_layer_norm = LayerNorm(self.embed_dim)
        self.fc1 = nn.Linear(self.embed_dim, config.decoder_ffn_dim)
        self.fc2 = nn.Linear(config.decoder_ffn_dim, self.embed_dim)
        self.final_layer_norm = LayerNorm(self.embed_dim)
```

在初始化方法中，设置了类的属性，包括嵌入维度、自注意力机制和交叉注意力机制的配置、Dropout 概率、激活函数、层归一化和线性层等。

```python
    def forward(
        self,
        x,
        encoder_hidden_states,
        encoder_attn_mask=None,
        layer_state=None,
        causal_mask=None,
        layer_head_mask=None,
        cross_attn_layer_head_mask=None,
        decoder_padding_mask=None,
        output_attentions=False,
    ):
```

定义了前向传播方法，接收多个输入参数。

```python
        residual = x

        if layer_state is None:
            layer_state = {}
```

保存输入 `x` 作为残差，并处理 `layer_state` 。

```python
        # Self Attention
        x, self_attn_weights = self.self_attn(
            query=x,
            key=x,
            layer_state=layer_state,  # adds keys to layer state
            key_padding_mask=decoder_padding_mask,
            attn_mask=causal_mask,
            layer_head_mask=layer_head_mask,
            output_attentions=output_attentions,
        )
        x = nn.functional.dropout(x, p=self.dropout, training=self.training)
        x = residual + x
        x = self.self_attn_layer_norm(x)
```

进行自注意力计算，应用 Dropout ，加上残差并进行层归一化。

```python
        # Cross attention
        residual = x
        assert self.encoder_attn.cache_key!= self.self_attn.cache_key
        x, cross_attn_weights = self.encoder_attn(
            query=x,
            key=encoder_hidden_states,
            key_padding_mask=encoder_attn_mask,
            layer_state=layer_state,  # mutates layer state
            layer_head_mask=cross_attn_layer_head_mask,
            output_attentions=output_attentions,
        )
        x = nn.functional.dropout(x, p=self.dropout, training=self.training)
        x = residual + x
        x = self.encoder_attn_layer_norm(x)
```

进行交叉注意力计算，同样进行相关处理。

```python
        # Fully Connected
        residual = x
        x = self.activation_fn(self.fc1(x))
        x = nn.functional.dropout(x, p=self.activation_dropout, training=self.training)
        x = self.fc2(x)
        x = nn.functional.dropout(x, p=self.dropout, training=self.training)
        x = residual + x
        x = self.final_layer_norm(x)
        return (
            x,
            self_attn_weights,
            layer_state,
            cross_attn_weights,
        )  # layer_state = cache for decoding
```

进行全连接层计算，加上残差并进行最终的层归一化，最后返回输出 `x` 、自注意力权重、层状态和交叉注意力权重。


```python
def _reorder_buffer(attn_cache, new_order):
    for k, input_buffer_k in attn_cache.items():
        if input_buffer_k is not None:
            attn_cache[k] = input_buffer_k.index_select(0, new_order)
    return attn_cache
```

以下是对这段代码的解释：

`_reorder_buffer` 函数的作用是对注意力缓存（`attn_cache`）中的数据按照新的顺序（`new_order`）进行重新排列。

它通过遍历 `attn_cache` 中的每个键值对。对于每个非空的值（`input_buffer_k`），使用 `index_select` 方法按照 `new_order` 对其进行重新索引，从而实现数据的重新排序。最后，函数返回重新排序后的 `attn_cache` 。



以下是对这两段代码的解释：

```python
def fill_with_neg_inf(t):
    """FP16-compatible function that fills a input_ids with -inf."""
    return t.float().fill_(float("-inf")).type_as(t)
```

这个函数 `fill_with_neg_inf` 接受一个张量 `t` ，首先将其转换为浮点数类型，然后用负无穷填充，最后再转换回与输入 `t` 相同的数据类型并返回。这样做是为了确保在处理不同数据类型（特别是与 FP16 兼容）时能够正确地填充负无穷值。

```python
# Public API
def _get_shape(t):
    return getattr(t, "shape", None)
```

这个函数 `_get_shape` 用于获取输入张量 `t` 的形状。它使用 Python 的内建函数 `getattr` 来获取 `t` 的 `shape` 属性，如果 `t` 没有 `shape` 属性，则返回 `None` 。


```python
```python
class Attention(nn.Module):
    """Multi-headed attention from 'Attention Is All You Need' paper"""

    def __init__(
        self,
        embed_dim,
        num_heads,
        dropout=0.0,
        bias=True,
        encoder_decoder_attention=False  # otherwise self_attention
    ):
        """
        初始化Attention类

        参数：
        embed_dim (int)：嵌入维度
        num_heads (int)：注意力头的数量
        dropout (float, 可选)：Dropout概率，默认为0.0
        bias (bool, 可选)：是否使用偏置，默认为True
        encoder_decoder_attention (bool, 可选)：是否为编码器-解码器注意力，否则为自注意力，默认为False
        """
        super().__init__()
        self.embed_dim = embed_dim  # 嵌入维度
        self.num_heads = num_heads  # 注意力头的数量
        self.dropout = dropout  # Dropout概率
        self.head_dim = embed_dim // num_heads  # 每个头的维度
        assert self.head_dim * num_heads == self.embed_dim, "embed_dim must be divisible by num_heads"  # 确保嵌入维度能被头数整除
        self.scaling = self.head_dim**-0.5  # 缩放因子

        self.encoder_decoder_attention = encoder_decoder_attention  # 编码器-解码器注意力标志
        self.k_proj = nn.Linear(embed_dim, embed_dim, bias=bias)  # 键的线性投影层
        self.v_proj = nn.Linear(embed_dim, embed_dim, bias=bias)  # 值的线性投影层
        self.q_proj = nn.Linear(embed_dim, embed_dim, bias=bias)  # 查询的线性投影层
        self.out_proj = nn.Linear(embed_dim, embed_dim, bias=bias)  # 输出的线性投影层
        self.cache_key = "encoder_decoder" if self.encoder_decoder_attention else "self"  # 缓存键

    def _shape(self, tensor, seq_len, bsz):
        """
        对输入张量进行形状变换

        参数：
        tensor (Tensor)：输入张量
        seq_len (int)：序列长度
        bsz (int)：批量大小

        返回：
        变换后的张量
        """
        return tensor.contiguous().view(seq_len, bsz * self.num_heads, self.head_dim).transpose(0, 1)

    def forward(
        self,
        query,
        key: Optional[Tensor],
        key_padding_mask: Optional[Tensor] = None,
        layer_state: Optional[Dict[str, Optional[Tensor]]] = None,
        attn_mask: Optional[Tensor] = None,
        layer_head_mask: Optional[Tensor] = None,
        output_attentions=False
    ) -> Tuple[Tensor, Optional[Tensor]]:
        """
        前向传播

        参数：
        query (Tensor)：查询张量
        key (Optional[Tensor])：键张量，可为None
        key_padding_mask (Optional[Tensor], 可选)：键的填充掩码，可为None
        layer_state (Optional[Dict[str, Optional[Tensor]]], 可选)：层状态，可为None
        attn_mask (Optional[Tensor], 可选)：注意力掩码，可为None
        layer_head_mask (Optional[Tensor], 可选)：层头掩码，可为None
        output_attentions (bool, 可选)：是否输出注意力权重，默认为False

        返回：
        attn_output (Tensor)：注意力输出
        attn_weights_reshaped (Optional[Tensor])：重塑后的注意力权重（如果output_attentions为True）
        """
        """Input shape: Time(SeqLen) x Batch x Channel"""
        static_kv: bool = self.encoder_decoder_attention  # 是否为静态键值对（编码器-解码器注意力）
        tgt_len, bsz, embed_dim = query.size()  # 获取查询的长度、批量大小和嵌入维度
        assert embed_dim == self.embed_dim  # 确保嵌入维度与当前类的一致
        assert list(query.size()) == [tgt_len, bsz, embed_dim]  # 进一步确认查询的形状

        # get here for encoder decoder cause of static_kv
        if layer_state is not None:  # 若存在层状态（用于重用键、值和编码器填充掩码）
            saved_state = layer_state.get(self.cache_key, {})  # 从层状态中获取缓存
            if "prev_key" in saved_state and static_kv:
                # 如果有先前的键且为静态键值对，则无需重新计算键和值
                key = None
        else:
            saved_state = None
            layer_state = {}

        q = self.q_proj(query) * self.scaling  # 计算查询的投影并缩放
        if static_kv:
            if key is None:
                k = v = None
            else:
                k = self.k_proj(key)
                v = self.v_proj(key)
        else:
            k = self.k_proj(query)
            v = self.v_proj(query)

        q = self._shape(q, tgt_len, bsz)  # 对查询进行形状变换
        if k is not None:
            k = self._shape(k, -1, bsz)
        if v is not None:
            v = self._shape(v, -1, bsz)

        if saved_state is not None:
            k, v, key_padding_mask = self._use_saved_state(k, v, saved_state, key_padding_mask, static_kv, bsz)

        # Update cache
        layer_state[self.cache_key] = {
            "prev_key": k.view(bsz, self.num_heads, -1, self.head_dim),
            "prev_value": v.view(bsz, self.num_heads, -1, self.head_dim),
            "prev_key_padding_mask": key_padding_mask if not static_kv else None,
        }

        assert k is not None
        src_len = k.size(1)  # 源序列长度
        attn_weights = torch.bmm(q, k.transpose(1, 2))  # 计算注意力权重
        assert attn_weights.size() == (bsz * self.num_heads, tgt_len, src_len)  # 确认权重形状

        if attn_mask is not None:
            attn_weights = attn_weights.view(bsz, self.num_heads, tgt_len, src_len) + attn_mask
            attn_weights = attn_weights.view(bsz * self.num_heads, tgt_len, src_len)

        # This is part of a workaround to get around fork/join parallelism not supporting Optional types.
        if key_padding_mask is not None and key_padding_mask.dim() == 0:
            key_padding_mask = None
        assert key_padding_mask is None or key_padding_mask.size()[:2] == (
            bsz,
            src_len,
        )

        if key_padding_mask is not None:  # 若存在键填充掩码
            attn_weights = attn_weights.view(bsz, self.num_heads, tgt_len, src_len)
            reshaped = key_padding_mask.unsqueeze(1).unsqueeze(2)
            attn_weights = attn_weights.masked_fill(reshaped, float("-inf"))  # 对掩码位置的权重设置为负无穷
            attn_weights = attn_weights.view(bsz * self.num_heads, tgt_len, src_len)

        attn_weights = nn.functional.softmax(attn_weights, dim=-1)  # 对权重进行Softmax归一化

        if layer_head_mask is not None:
            assert layer_head_mask.size() == (
                self.num_heads,
            ), f"Head mask for a single layer should be of size {(self.num_heads,)}, but is {layer_head_mask.size()}"
            attn_weights = layer_head_mask.view(1, -1, 1, 1) * attn_weights.view(bsz, self.num_heads, tgt_len, src_len)
            attn_weights = attn_weights.view(bsz * self.num_heads, tgt_len, src_len)

        if output_attentions:
            # make sure that attn_weights are included in graph
            attn_weights_reshaped = attn_weights.view(bsz, self.num_heads, tgt_len, src_len)
            attn_weights = attn_weights_reshaped.view(bsz * self.num_heads, tgt_len, src_len)
        else:
            attn_weights_reshaped = None

        attn_probs = nn.functional.dropout(
            attn_weights,
            p=self.dropout,
            training=self.training,
        )  # 对注意力权重应用Dropout

        assert v is not None
        attn_output = torch.bmm(attn_probs, v)  # 计算注意力输出
        assert attn_output.size() == (bsz * self.num_heads, tgt_len, self.head_dim)
        attn_output = attn_output.transpose(0, 1).contiguous().view(tgt_len, bsz, embed_dim)  # 对输出进行形状变换
        attn_output = self.out_proj(attn_output)  # 通过输出投影层

        return attn_output, attn_weights_reshaped  # 返回注意力输出和（可选的）注意力权重

    def _use_saved_state(self, k, v, saved_state, key_padding_mask, static_kv, bsz):
        """
        使用保存的状态

        参数：
        k (Tensor)：当前计算的键张量
        v (Tensor)：当前计算的值张量
        saved_state (Dict)：保存的状态
        key_padding_mask (Tensor)：键的填充掩码
        static_kv (bool)：是否为静态键值对
        bsz (int)：批量大小

        返回：
        k (Tensor)：更新后的键张量
        v (Tensor)：更新后的值张量
        new_key_padding_mask (Tensor)：更新后的键填充掩码
        """
        # saved states are stored with shape (bsz, num_heads, seq_len, head_dim)
        if "prev_key" in saved_state:
            _prev_key = saved_state["prev_key"]
            assert _prev_key is not None
            prev_key = _prev_key.view(bsz * self.num_heads, -1, self.head_dim)
            if static_kv:
                k = prev_key
            else:
                assert k is not None
                k = torch.cat([prev_key, k], dim=1)
        if "prev_value" in saved_state:
            _prev_value = saved_state["prev_value"]
            assert _prev_value is not None
            prev_value = _prev_value.view(bsz * self.num_heads, -1, self.head_dim)
            if static_kv:
                v = prev_value
            else:
                assert v is not None
                v = torch.cat([prev_value, v], dim=1)
        assert k is not None and v is not None
        prev_key_padding_mask: Optional[Tensor] = saved_state.get("prev_key_padding_mask", None)
        if prev_key_padding_mask is not None:
            if static_kv:
                new_key_padding_mask = prev_key_padding_mask
            else:
                new_key_padding_mask = torch.cat([prev_key_padding_mask, key_padding_mask], dim=1)
        else:
            new_key_padding_mask = key_padding_mask
        return k, v, new_key_padding_mask
```



```python
@add_start_docstrings(
    "The bare FSMT Model outputting raw hidden-states without any specific head on top.",
    FSMT_START_DOCSTRING,
)
class FSMTModel(PretrainedFSMTModel):
    """
    定义了 FSMTModel 类，继承自 PretrainedFSMTModel

    初始化：
    - 接收 FSMTConfig 类型的配置对象
    - 定义编码器和解码器的嵌入层
    - 初始化编码器和解码器

    前向传播（forward 方法）：
    - 处理解码器输入 ID 的默认情况
    - 处理输出相关参数的默认值
    - 根据是否使用缓存准备解码器输入
    - 如果编码器输出不存在则计算
    - 计算解码器输出
    - 根据是否返回字典格式进行不同的返回

    其他方法：
    - `get_input_embeddings`：获取输入嵌入层
    - `set_input_embeddings`：设置输入嵌入层
    - `get_output_embeddings`：获取输出嵌入层
    - `set_output_embeddings`：设置输出嵌入层
    """

    def __init__(self, config: FSMTConfig):
        """
        初始化 FSMTModel 类

        参数：
        config (FSMTConfig)：FSMT 模型的配置对象
        """
        super().__init__(config)

        padding_idx = config.pad_token_id
        encoder_embed_tokens = nn.Embedding(config.src_vocab_size, config.d_model, padding_idx)
        decoder_embed_tokens = nn.Embedding(config.tgt_vocab_size, config.d_model, padding_idx)

        self.encoder = FSMTEncoder(config, encoder_embed_tokens)
        self.decoder = FSMTDecoder(config, decoder_embed_tokens)

        # Initialize weights and apply final processing
        self.post_init()

    @add_start_docstrings_to_model_forward(FSMT_INPUTS_DOCSTRING)
    @add_code_sample_docstrings(
        processor_class=_TOKENIZER_FOR_DOC,
        checkpoint=_CHECKPOINT_FOR_DOC,
        output_type=Seq2SeqModelOutput,
        config_class=_CONFIG_FOR_DOC,
    )
    def forward(
        self,
        input_ids,
        attention_mask=None,
        decoder_input_ids=None,
        decoder_attention_mask=None,
        head_mask=None,
        decoder_head_mask=None,
        cross_attn_head_mask=None,
        encoder_outputs: Optional[Tuple] = None,
        past_key_values=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        """
        前向传播方法

        参数：
        input_ids (Tensor)：输入的标记 ID
        attention_mask (Tensor, 可选)：注意力掩码
        decoder_input_ids (Tensor, 可选)：解码器的输入标记 ID
        decoder_attention_mask (Tensor, 可选)：解码器的注意力掩码
        head_mask (Tensor, 可选)：编码器的头掩码
        decoder_head_mask (Tensor, 可选)：解码器的头掩码
        cross_attn_head_mask (Tensor, 可选)：交叉注意力的头掩码
        encoder_outputs (Tuple, 可选)：编码器的输出
        past_key_values (Any, 可选)：过去的键值对
        use_cache (bool, 可选)：是否使用缓存
        output_attentions (bool, 可选)：是否输出注意力
        output_hidden_states (bool, 可选)：是否输出隐藏状态
        return_dict (bool, 可选)：是否返回字典格式

        返回：
        根据 return_dict 的值返回不同的结果
        """
        if decoder_input_ids is None:
            use_cache = False

        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        # make masks if user doesn't supply
        if not use_cache:
            decoder_input_ids, decoder_padding_mask, causal_mask = _prepare_fsmt_decoder_inputs(
                self.config,
                input_ids,
                decoder_input_ids=decoder_input_ids,
                decoder_padding_mask=decoder_attention_mask,
                causal_mask_dtype=self.decoder.embed_tokens.weight.dtype,
            )
        else:
            decoder_padding_mask, causal_mask = None, None

        assert decoder_input_ids is not None

        if encoder_outputs is None:
            encoder_outputs = self.encoder(
                input_ids=input_ids,
                attention_mask=attention_mask,
                head_mask=head_mask,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                return_dict=return_dict,
            )
        # If the user passed a tuple for encoder_outputs, we wrap it in a BaseModelOutput when return_dict=False
        elif return_dict and not isinstance(encoder_outputs, BaseModelOutput):
            encoder_outputs = BaseModelOutput(
                last_hidden_state=encoder_outputs[0],
                hidden_states=encoder_outputs[1] if len(encoder_outputs) > 1 else None,
                attentions=encoder_outputs[2] if len(encoder_outputs) > 2 else None,
            )

        # decoder outputs consists of (dec_features, layer_state, dec_hidden, dec_attn)
        decoder_outputs = self.decoder(
            decoder_input_ids,
            encoder_outputs[0],
            attention_mask,
            decoder_padding_mask,
            decoder_causal_mask=causal_mask,
            head_mask=decoder_head_mask,
            cross_attn_head_mask=cross_attn_head_mask,
            past_key_values=past_key_values,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        if not return_dict:
            return decoder_outputs + encoder_outputs

        return Seq2SeqModelOutput(
            last_hidden_state=decoder_outputs.last_hidden_state,
            past_key_values=decoder_outputs.past_key_values,
            decoder_hidden_states=decoder_outputs.hidden_states,
            decoder_attentions=decoder_outputs.attentions,
            cross_attentions=decoder_outputs.cross_attentions,
            encoder_last_hidden_state=encoder_outputs.last_hidden_state,
            encoder_hidden_states=encoder_outputs.hidden_states,
            encoder_attentions=encoder_outputs.attentions,
        )

    def get_input_embeddings(self):
        """
        获取输入嵌入层

        返回：
        编码器的嵌入层
        """
        return self.encoder.embed_tokens

    def set_input_embeddings(self, value):
        """
        设置输入嵌入层

        参数：
        value (nn.Embedding)：新的嵌入层
        """
        self.encoder.embed_tokens = value

    def get_output_embeddings(self):
        """
        获取输出嵌入层

        返回：
        解码器的嵌入层
        """
        return self.decoder.embed_tokens

    def set_output_embeddings(self, value):
        """
        设置输出嵌入层

        参数：
        value (nn.Embedding)：新的嵌入层
        """
        self.decoder.embed_tokens = value
```



```python
@add_start_docstrings(
    "The FSMT Model with a language modeling head. Can be used for summarization.", FSMT_START_DOCSTRING
)
class FSMTForConditionalGeneration(PretrainedFSMTModel):
    """
    定义了 FSMTForConditionalGeneration 类，继承自 PretrainedFSMTModel

    属性：
    - `base_model_prefix`：模型的基础前缀
    - `_keys_to_ignore_on_load_missing`：加载时忽略缺失的键
    - `_keys_to_ignore_on_save`：保存时忽略的键

    初始化：
    - 接收 FSMTConfig 类型的配置对象
    - 创建 FSMTModel 作为基础模型

    前向传播（forward 方法）：
    - 处理返回字典格式
    - 如果有标签，设置不使用缓存
    - 获取基础模型的输出
    - 计算掩码语言模型损失（如果有标签）
    - 根据是否返回字典格式进行不同的返回

    其他方法：
    - `prepare_inputs_for_generation`：准备生成所需的输入
    - `prepare_decoder_input_ids_from_labels`：从标签准备解码器输入 ID
    - `_reorder_cache`：重新排序缓存
    - `get_encoder`：获取编码器
    - `get_output_embeddings`：获取输出嵌入层
    - `set_output_embeddings`：设置输出嵌入层
    """

    base_model_prefix = "model"
    _keys_to_ignore_on_load_missing = [
        "model.encoder.embed_positions.weight",
        "model.decoder.embed_positions.weight",
    ]
    _keys_to_ignore_on_save = [
        "model.encoder.embed_positions.weight",
        "model.decoder.embed_positions.weight",
    ]

    def __init__(self, config: FSMTConfig):
        """
        初始化 FSMTForConditionalGeneration 类

        参数：
        config (FSMTConfig)：FSMT 模型的配置对象
        """
        super().__init__(config)
        base_model = FSMTModel(config)
        self.model = base_model

    @add_start_docstrings_to_model_forward(FSMT_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=Seq2SeqLMOutput, config_class=_CONFIG_FOR_DOC)
    @add_end_docstrings(FSMT_GENERATION_EXAMPLE)
    def forward(
        self,
        input_ids,
        attention_mask=None,
        decoder_input_ids=None,
        decoder_attention_mask=None,
        head_mask=None,
        decoder_head_mask=None,
        cross_attn_head_mask=None,
        encoder_outputs=None,
        past_key_values=None,
        labels=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        """
        前向传播方法

        参数：
        input_ids (Tensor)：输入的标记 ID
        attention_mask (Tensor, 可选)：注意力掩码
        decoder_input_ids (Tensor, 可选)：解码器的输入标记 ID
        decoder_attention_mask (Tensor, 可选)：解码器的注意力掩码
        head_mask (Tensor, 可选)：编码器的头掩码
        decoder_head_mask (Tensor, 可选)：解码器的头掩码
        cross_attn_head_mask (Tensor, 可选)：交叉注意力的头掩码
        encoder_outputs (Tuple, 可选)：编码器的输出
        past_key_values (Any, 可选)：过去的键值对
        labels (Tensor, 可选)：用于计算掩码语言模型损失的标签
        use_cache (bool, 可选)：是否使用缓存
        output_attentions (bool, 可选)：是否输出注意力
        output_hidden_states (bool, 可选)：是否输出隐藏状态
        return_dict (bool, 可选)：是否返回字典格式

        返回：
        根据条件返回不同的结果
        """
        r"""
        labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
            Labels for computing the masked language modeling loss. Indices should either be in `[0,...,
            config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
            (masked), the loss is only computed for the tokens with labels in `[0,..., config.vocab_size]`.

        Returns:

        """
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if labels is not None:
            use_cache = False

        outputs = self.model(
            input_ids,
            attention_mask=attention_mask,
            decoder_input_ids=decoder_input_ids,
            encoder_outputs=encoder_outputs,
            decoder_attention_mask=decoder_attention_mask,
            head_mask=head_mask,
            decoder_head_mask=decoder_head_mask,
            cross_attn_head_mask=cross_attn_head_mask,
            past_key_values=past_key_values,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        lm_logits = outputs[0]

        masked_lm_loss = None
        if labels is not None:
            loss_fct = CrossEntropyLoss()
            # TODO(SS): do we need to ignore pad tokens in labels?
            masked_lm_loss = loss_fct(lm_logits.view(-1, self.config.tgt_vocab_size), labels.view(-1))

        if not return_dict:
            output = (lm_logits,) + outputs[1:]
            return ((masked_lm_loss,) + output) if masked_lm_loss is not None else output

        return Seq2SeqLMOutput(
            loss=masked_lm_loss,
            logits=lm_logits,
            past_key_values=outputs.past_key_values,
            decoder_hidden_states=outputs.decoder_hidden_states,
            decoder_attentions=outputs.decoder_attentions,
            cross_attentions=outputs.cross_attentions,
            encoder_last_hidden_state=outputs.encoder_last_hidden_state,
            encoder_hidden_states=outputs.encoder_hidden_states,
            encoder_attentions=outputs.encoder_attentions,
        )

    def prepare_inputs_for_generation(
        self,
        decoder_input_ids,
        past=None,
        attention_mask=None,
        head_mask=None,
        decoder_head_mask=None,
        cross_attn_head_mask=None,
        use_cache=None,
        encoder_outputs=None,
        **kwargs
    ):
        """
        准备生成所需的输入

        参数：
        decoder_input_ids (Tensor)：解码器的输入标记 ID
        past (Any, 可选)：过去的状态
        attention_mask (Tensor, 可选)：注意力掩码
        head_mask (Tensor, 可选)：编码器的头掩码
        decoder_head_mask (Tensor, 可选)：解码器的头掩码
        cross_attn_head_mask (Tensor, 可选)：交叉注意力的头掩码
        use_cache (bool, 可选)：是否使用缓存
        encoder_outputs (Tuple, 可选)：编码器的输出
        **kwargs：其他关键字参数

        返回：
        包含准备好的输入的字典
        """
        return {
            "input_ids": None,  # encoder_outputs is defined. input_ids not needed
            "encoder_outputs": encoder_outputs,
            "past_key_values": past,
            "decoder_input_ids": decoder_input_ids,
            "attention_mask": attention_mask,
            "head_mask": head_mask,
            "decoder_head_mask": decoder_head_mask,
            "cross_attn_head_mask": cross_attn_head_mask,
            "use_cache": use_cache,  # change this to avoid caching (presumably for debugging)
        }

    def prepare_decoder_input_ids_from_labels(self, labels: torch.Tensor):
        """
        从标签准备解码器输入 ID

        参数：
        labels (torch.Tensor)：标签张量

        返回：
        处理后的解码器输入 ID
        """
        return shift_tokens_right(labels, self.config.pad_token_id)

    @staticmethod
    def _reorder_cache(past, beam_idx):
        """
        重新排序缓存

        参数：
        past (List)：过去的缓存
        beam_idx (Tensor)：波束索引

        返回：
        重新排序后的缓存列表
        """
        reordered_past = []
        for layer_past in past:
            # get the correct batch idx from decoder layer's batch dim for cross and self-attn
            layer_past_new = {
                attn_key: _reorder_buffer(attn_cache, beam_idx) for attn_key, attn_cache in layer_past.items()
            }
            reordered_past.append(layer_past_new)
        return reordered_past

    def get_encoder(self):
        """
        获取编码器

        返回：
        模型的编码器
        """
        return self.model.encoder

    def get_output_embeddings(self):
        """
        获取输出嵌入层

        返回：
        模型解码器的嵌入层
        """
        return self.model.decoder.embed_tokens

    def set_output_embeddings(self, value):
        """
        设置输出嵌入层

        参数：
        value (nn.Embedding)：新的嵌入层
        """
        self.model.decoder.embed_tokens = value
```



```python
class SinusoidalPositionalEmbedding(nn.Embedding):
    """
    这个类实现了正弦位置嵌入。

    特点和行为：
    - 不保存嵌入的权重，因为它是确定性的且可能很大。
    - 填充符号会被忽略。
    - 嵌入会在需要更多位置时自动扩展。

    初始化：
    - 接收位置数量、嵌入维度和填充索引来构建权重。

    方法：
    - `make_weight`：创建并设置嵌入的权重。
    - `get_embedding`：静态方法，用于生成正弦位置嵌入。
    - `make_positions`：静态方法，将非填充符号替换为其位置编号。
    - `forward`：前向传播方法，处理输入并获取相应的位置嵌入。
    """

    def __init__(self, num_positions, embedding_dim, padding_idx):
        """
        初始化类，调用`make_weight`方法来创建并设置权重

        参数：
        num_positions (int)：可能的最大位置数量
        embedding_dim (int)：每个位置嵌入的维度
        padding_idx (int)：用于表示填充的索引
        """
        self.make_weight(num_positions, embedding_dim, padding_idx)

    def make_weight(self, num_positions, embedding_dim, padding_idx):
        """
        创建位置嵌入的权重

        参数：
        num_positions (int)：可能的最大位置数量
        embedding_dim (int)：每个位置嵌入的维度
        padding_idx (int)：用于表示填充的索引

        过程：
        1. 通过`get_embedding`方法获取嵌入的权重值`weight`。
        2. 如果类中还没有`weight`属性（即在初始化时），通过父类`nn.Embedding`的初始化来设置权重。
        3. 否则，将新生成的权重值转换为与已有`weight`相同的数据类型和设备，并将其设置为参数。
        4. 分离权重，使其不参与梯度计算，且不需要梯度。
        """
        weight = self.get_embedding(num_positions, embedding_dim, padding_idx)
        if not hasattr(self, "weight"):
            # 在 __init__ 中
            super().__init__(num_positions, embedding_dim, padding_idx, _weight=weight)
        else:
            # 在 forward 中，将权重设置为正确的数据类型和设备
            weight = weight.to(dtype=self.weight.dtype, device=self.weight.device)
            self.weight = nn.Parameter(weight)
        self.weight.detach_()
        self.weight.requires_grad = False

    @staticmethod
    def get_embedding(num_embeddings, embedding_dim, padding_idx):
        """
        静态方法，用于生成正弦位置嵌入的权重值

        参数：
        num_embeddings (int)：位置嵌入的数量
        embedding_dim (int)：每个位置嵌入的维度
        padding_idx (int)：用于表示填充的索引

        过程：
        1. 计算嵌入维度的一半`half_dim`。
        2. 计算用于生成正弦波的系数`emb`。
        3. 生成位置索引的张量。
        4. 通过正弦和余弦函数生成位置嵌入，并连接起来。
        5. 如果嵌入维度是奇数，进行零填充。
        6. 如果有指定的填充索引，将对应位置的嵌入值设为 0。

        返回：
        生成的位置嵌入权重张量
        """
        """
        Build sinusoidal embeddings.

        This matches the implementation in tensor2tensor, but differs slightly from the description in Section 3.5 of
        "Attention Is All You Need".
        """
        half_dim = embedding_dim // 2
        emb = math.log(10000) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim, dtype=torch.float) * -emb)
        emb = torch.arange(num_embeddings, dtype=torch.float).unsqueeze(1) * emb.unsqueeze(0)
        emb = torch.cat([torch.sin(emb), torch.cos(emb)], dim=1).view(num_embeddings, -1)
        if embedding_dim % 2 == 1:
            # 零填充
            emb = torch.cat([emb, torch.zeros(num_embeddings, 1)], dim=1)
        if padding_idx is not None:
            emb[padding_idx, :] = 0
        return emb

    @staticmethod
    def make_positions(tensor, padding_idx: int):
        """
        静态方法，将输入张量中非填充符号替换为其位置编号

        参数：
        tensor (Tensor)：输入张量，可能包含填充符号
        padding_idx (int)：用于表示填充的索引

        过程：
        1. 创建一个与输入张量相同形状的掩码张量，其中非填充符号对应位置为 1，填充符号对应位置为 0。
        2. 按列计算累积和，得到每个位置的累计数。
        3. 将累积数乘以掩码，得到非填充符号的位置编号。
        4. 加上填充索引的值，得到最终的位置编号。

        返回：
        包含位置编号的张量
        """
        """
        Replace non-padding symbols with their position numbers.

        Position numbers begin at padding_idx+1. Padding symbols are ignored.
        """
        # The series of casts and type-conversions here are carefully
        # balanced to both work with ONNX export and XLA. In particular XLA
        # prefers ints, cumsum defaults to output longs, and ONNX doesn't know
        # how to handle the dtype kwarg in cumsum.
        mask = tensor.ne(padding_idx).int()
        return (torch.cumsum(mask, dim=1).type_as(mask) * mask).long() + padding_idx

    def forward(
        self,
        input,
        incremental_state: Optional[Any] = None,
        timestep: Optional[Tensor] = None,
    ):
        """
        前向传播方法

        参数：
        input (Tensor)：输入张量，预期形状为 [bsz x seqlen]，表示序列
        incremental_state (Any, 可选)：增量状态，可能用于处理序列的逐步生成
        timestep (Tensor, 可选)：时间步，可能用于特定的时间相关操作

        过程：
        1. 获取输入的批量大小`bsz`和序列长度`seq_len`。
        2. 计算最大可能需要的位置`max_pos`，即填充索引加上 1 再加上当前序列长度。
        3. 如果最大位置超过了已有的权重大小，调用`make_weight`方法扩展权重。
        4. 通过`make_positions`方法将输入中的非填充符号转换为位置编号。
        5. 调用父类`nn.Embedding`的前向传播方法，获取对应的位置嵌入。

        返回：
        与输入对应的位置嵌入
        """
        """Input is expected to be of size [bsz x seqlen]."""
        bsz, seq_len = input.shape[:2]
        max_pos = self.padding_idx + 1 + seq_len
        if max_pos > self.weight.size(0):
            # 扩展嵌入如果需要
            self.make_weight(max_pos, self.embedding_dim, self.padding_idx)
        positions = self.make_positions(input, self.padding_idx)
        return super().forward(positions)
```
